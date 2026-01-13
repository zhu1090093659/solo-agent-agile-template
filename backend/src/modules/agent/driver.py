"""
Claude Code Driver

Drives the agent using Claude Code CLI as the underlying engine.
This allows leveraging Claude Code's agentic capabilities:
- Code execution
- File operations
- Tool use
- Multi-turn conversations
"""

import asyncio
import subprocess
import json
import os
from typing import AsyncIterator, Optional
from pathlib import Path
from dataclasses import dataclass
from ..config.settings import settings


@dataclass
class ClaudeCodeConfig:
    """Configuration for Claude Code."""
    model: str = "sonnet"  # or "opus", "haiku"
    max_turns: int = 10
    timeout: int = 300  # 5 minutes
    workspace: Optional[Path] = None
    system_prompt_file: Optional[Path] = None


class ClaudeCodeDriver:
    """
    Driver for Claude Code CLI.
    
    Executes claude commands and streams output back.
    Each session runs in an isolated workspace.
    """
    
    def __init__(self, config: Optional[ClaudeCodeConfig] = None):
        self.config = config or ClaudeCodeConfig()
        self.base_workspace = Path(settings.AGENT_WORKSPACE_DIR)
        self.base_workspace.mkdir(parents=True, exist_ok=True)
    
    def _get_session_workspace(self, session_id: str) -> Path:
        """Get or create workspace directory for a session."""
        workspace = self.base_workspace / session_id
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace
    
    def _build_command(
        self,
        message: str,
        session_id: str,
        system_prompt: Optional[str] = None,
        continue_conversation: bool = False,
        allowed_tools: Optional[list[str]] = None,
    ) -> list[str]:
        """Build the claude CLI command."""
        cmd = ["claude"]
        
        # Add message
        cmd.extend(["--print", message])
        
        # Model selection
        if self.config.model:
            cmd.extend(["--model", self.config.model])
        
        # Max turns for agentic behavior
        cmd.extend(["--max-turns", str(self.config.max_turns)])
        
        # Output format - JSON for structured parsing
        cmd.extend(["--output-format", "stream-json"])
        
        # System prompt
        if system_prompt:
            cmd.extend(["--system-prompt", system_prompt])
        elif self.config.system_prompt_file:
            cmd.extend(["--system-prompt-file", str(self.config.system_prompt_file)])
        
        # Continue previous conversation
        if continue_conversation:
            cmd.append("--continue")
        
        # Allowed tools (if restricted)
        if allowed_tools:
            for tool in allowed_tools:
                cmd.extend(["--allowedTools", tool])
        
        # Disable interactive prompts
        cmd.append("--no-interactive")
        
        return cmd
    
    async def execute(
        self,
        message: str,
        session_id: str,
        system_prompt: Optional[str] = None,
        continue_conversation: bool = False,
        allowed_tools: Optional[list[str]] = None,
    ) -> AsyncIterator[dict]:
        """
        Execute a message through Claude Code.
        
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
            - {"type": "tool_result", "tool": "...", "output": "..."}
            - {"type": "error", "message": "..."}
            - {"type": "done", "usage": {...}}
        """
        workspace = self._get_session_workspace(session_id)
        
        cmd = self._build_command(
            message=message,
            session_id=session_id,
            system_prompt=system_prompt,
            continue_conversation=continue_conversation,
            allowed_tools=allowed_tools,
        )
        
        # Set up environment
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(workspace),
                env=env,
            )
            
            # Stream stdout
            async for line in self._read_stream(process.stdout):
                event = self._parse_event(line)
                if event:
                    yield event
            
            # Wait for completion
            await asyncio.wait_for(
                process.wait(),
                timeout=self.config.timeout
            )
            
            # Check for errors
            if process.returncode != 0:
                stderr = await process.stderr.read()
                yield {
                    "type": "error",
                    "message": stderr.decode() if stderr else f"Process exited with code {process.returncode}"
                }
            
            yield {"type": "done"}
            
        except asyncio.TimeoutError:
            yield {
                "type": "error",
                "message": f"Execution timed out after {self.config.timeout}s"
            }
        except FileNotFoundError:
            yield {
                "type": "error", 
                "message": "Claude Code CLI not found. Please install: npm install -g @anthropic-ai/claude-code"
            }
        except Exception as e:
            yield {
                "type": "error",
                "message": str(e)
            }
    
    async def _read_stream(self, stream) -> AsyncIterator[str]:
        """Read lines from async stream."""
        while True:
            line = await stream.readline()
            if not line:
                break
            yield line.decode().strip()
    
    def _parse_event(self, line: str) -> Optional[dict]:
        """Parse a JSON event from Claude Code output."""
        if not line:
            return None
        
        try:
            data = json.loads(line)
            
            # Map Claude Code events to our format
            event_type = data.get("type", "")
            
            if event_type == "assistant":
                # Assistant text message
                return {
                    "type": "text",
                    "content": data.get("message", "")
                }
            
            elif event_type == "tool_use":
                return {
                    "type": "tool_use",
                    "tool": data.get("tool", ""),
                    "input": data.get("input", {})
                }
            
            elif event_type == "tool_result":
                return {
                    "type": "tool_result",
                    "tool": data.get("tool", ""),
                    "output": data.get("output", "")
                }
            
            elif event_type == "error":
                return {
                    "type": "error",
                    "message": data.get("message", "Unknown error")
                }
            
            elif event_type == "result":
                return {
                    "type": "done",
                    "usage": data.get("usage", {})
                }
            
            # For text streaming
            elif "text" in data:
                return {
                    "type": "text",
                    "content": data["text"]
                }
            
            return None
            
        except json.JSONDecodeError:
            # Plain text output
            if line.strip():
                return {
                    "type": "text",
                    "content": line
                }
            return None
    
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
    
    def cleanup_session(self, session_id: str) -> None:
        """Clean up a session's workspace."""
        import shutil
        workspace = self.base_workspace / session_id
        if workspace.exists():
            shutil.rmtree(workspace)


# Default driver instance
claude_code_driver = ClaudeCodeDriver()
