"""
Claude Agent SDK Driver

Drives the agent using Claude Python Agent SDK as the underlying engine.
This allows leveraging Claude's agentic capabilities:
- Code execution
- File operations
- Tool use
- Multi-turn conversations
"""

from typing import AsyncIterator, Optional
from pathlib import Path
from dataclasses import dataclass

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
)

from ..config.settings import settings


@dataclass
class ClaudeSDKConfig:
    """Configuration for Claude SDK."""
    model: str = settings.claude_model
    max_turns: int = settings.agent_max_turns
    timeout: int = settings.agent_timeout
    workspace: Optional[Path] = None
    system_prompt_file: Optional[Path] = None
    permission_mode: str = settings.agent_permission_mode


class ClaudeSDKDriver:
    """
    Driver for Claude Agent SDK.
    
    Executes queries and streams output back.
    Each session runs in an isolated workspace.
    """
    
    def __init__(self, config: Optional[ClaudeSDKConfig] = None):
        self.config = config or ClaudeSDKConfig()
        # Use resolve() to convert relative path to absolute path
        self.base_workspace = Path(settings.AGENT_WORKSPACE_DIR).resolve()
        self.base_workspace.mkdir(parents=True, exist_ok=True)
        # Store active clients for session continuity
        self._clients: dict[str, ClaudeSDKClient] = {}
    
    def _get_session_workspace(self, session_id: str) -> Path:
        """Get or create workspace directory for a session."""
        workspace = self.base_workspace / session_id
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace
    
    def _build_options(
        self,
        session_id: str,
        system_prompt: Optional[str] = None,
        allowed_tools: Optional[list[str]] = None,
    ) -> ClaudeAgentOptions:
        """Build ClaudeAgentOptions for the query."""
        workspace = self._get_session_workspace(session_id)
        
        return ClaudeAgentOptions(
            system_prompt=system_prompt,
            allowed_tools=allowed_tools or [],
            permission_mode=self.config.permission_mode,
            max_turns=self.config.max_turns,
            model=self.config.model,
            cwd=str(workspace),
        )
    
    def _map_message(self, message) -> list[dict]:
        """Map SDK message to our event format."""
        events = []
        
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    events.append({
                        "type": "text",
                        "content": block.text
                    })
                elif isinstance(block, ToolUseBlock):
                    events.append({
                        "type": "tool_use",
                        "tool": block.name,
                        "input": block.input
                    })
                elif isinstance(block, ToolResultBlock):
                    # Extract content from tool result
                    content = block.content
                    if isinstance(content, list):
                        # Handle list of content blocks
                        output = ""
                        for item in content:
                            if isinstance(item, dict) and "text" in item:
                                output += item["text"]
                            elif isinstance(item, str):
                                output += item
                    elif isinstance(content, str):
                        output = content
                    else:
                        output = str(content) if content else ""
                    
                    events.append({
                        "type": "tool_result",
                        "tool_use_id": block.tool_use_id,
                        "output": output,
                        "is_error": block.is_error or False
                    })
        
        elif isinstance(message, ResultMessage):
            events.append({
                "type": "done",
                "session_id": message.session_id,
                "duration_ms": message.duration_ms,
                "is_error": message.is_error,
                "usage": message.usage,
                "total_cost_usd": message.total_cost_usd,
            })
        
        return events
    
    async def execute(
        self,
        message: str,
        session_id: str,
        system_prompt: Optional[str] = None,
        continue_conversation: bool = False,
        allowed_tools: Optional[list[str]] = None,
    ) -> AsyncIterator[dict]:
        """
        Execute a message through Claude SDK.
        
        Args:
            message: User message
            session_id: Session identifier for workspace isolation
            system_prompt: Optional system prompt override
            continue_conversation: Whether to continue previous conversation
            allowed_tools: List of allowed tools (None = all)
            
        Yields:
            Event dicts with structure:
            - {"type": "text", "content": "..."}
            - {"type": "tool_use", "tool": "...", "input": {...}}
            - {"type": "tool_result", "tool_use_id": "...", "output": "..."}
            - {"type": "error", "message": "..."}
            - {"type": "done", "usage": {...}}
        """
        try:
            options = self._build_options(
                session_id=session_id,
                system_prompt=system_prompt,
                allowed_tools=allowed_tools,
            )
            
            # Check if we should continue an existing session
            if continue_conversation and session_id in self._clients:
                client = self._clients[session_id]
                await client.query(message)
            else:
                # Create new client for this session
                client = ClaudeSDKClient(options=options)
                await client.connect()
                self._clients[session_id] = client
                await client.query(message)
            
            # Stream response
            async for msg in client.receive_response():
                events = self._map_message(msg)
                for event in events:
                    yield event
            
        except Exception as e:
            error_type = type(e).__name__
            yield {
                "type": "error",
                "message": f"{error_type}: {str(e)}"
            }
            # Cleanup on error
            if session_id in self._clients:
                try:
                    await self._clients[session_id].disconnect()
                except Exception:
                    pass
                del self._clients[session_id]
    
    async def execute_simple(
        self,
        message: str,
        session_id: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Execute and return full response as string.
        
        Convenience method for non-streaming use cases.
        """
        chunks = []
        async for event in self.execute(
            message=message,
            session_id=session_id,
            system_prompt=system_prompt,
        ):
            if event["type"] == "text":
                chunks.append(event["content"])
            elif event["type"] == "error":
                raise RuntimeError(event["message"])
        
        return "".join(chunks)
    
    async def cleanup_session(self, session_id: str) -> None:
        """Clean up a session's workspace and client."""
        # Disconnect client if exists
        if session_id in self._clients:
            try:
                await self._clients[session_id].disconnect()
            except Exception:
                pass
            del self._clients[session_id]
        
        # Remove workspace
        import shutil
        workspace = self.base_workspace / session_id
        if workspace.exists():
            shutil.rmtree(workspace)


# Default driver instance
claude_sdk_driver = ClaudeSDKDriver()
