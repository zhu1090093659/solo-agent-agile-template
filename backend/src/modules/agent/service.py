"""
Agent Service

High-level agent service that manages:
- System prompts and personas
- Session management
- Tool permissions
"""

from typing import AsyncIterator, Optional
from pathlib import Path
from .driver import claude_code_driver, ClaudeCodeConfig


class AgentService:
    """
    Main Agent Service.
    
    Wraps Claude Code driver with:
    - Prompt management
    - Session tracking
    - Tool permission control
    """
    
    def __init__(self):
        self.prompts_dir = Path(__file__).parent / "prompts"
        self.prompts_dir.mkdir(parents=True, exist_ok=True)
        self._system_prompt: Optional[str] = None
        self._persona: str = "default"
        
        # Tool permissions - customize which tools your agent can use
        # None means all tools allowed
        self.allowed_tools: Optional[list[str]] = None
        
        # Active sessions
        self._sessions: dict[str, dict] = {}
    
    @property
    def system_prompt(self) -> str:
        """Get current system prompt."""
        if self._system_prompt is None:
            self._system_prompt = self._load_prompt("system")
        return self._system_prompt
    
    def _load_prompt(self, name: str) -> str:
        """Load prompt from file."""
        prompt_file = self.prompts_dir / f"{name}.md"
        if prompt_file.exists():
            return prompt_file.read_text()
        return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """Default system prompt if none configured."""
        return """You are a helpful AI assistant.

Be concise and helpful. If you need to use tools, explain what you're doing.
"""
    
    def set_persona(self, persona: str) -> None:
        """
        Switch agent persona.
        
        Looks for persona file: prompts/persona_{name}.md
        """
        self._persona = persona
        base_prompt = self._load_prompt("system")
        
        persona_file = self.prompts_dir / f"persona_{persona}.md"
        if persona_file.exists():
            persona_content = persona_file.read_text()
            self._system_prompt = f"{base_prompt}\n\n## Persona\n\n{persona_content}"
        else:
            self._system_prompt = base_prompt
    
    def reload_prompt(self) -> None:
        """Force reload of system prompt."""
        self._system_prompt = None
    
    def set_allowed_tools(self, tools: Optional[list[str]]) -> None:
        """
        Set which tools the agent can use.
        
        Args:
            tools: List of tool names, or None for all tools
        """
        self.allowed_tools = tools
    
    def start_session(self, session_id: str) -> dict:
        """Start a new chat session."""
        self._sessions[session_id] = {
            "id": session_id,
            "message_count": 0,
            "created_at": None,  # Will be set on first message
        }
        return self._sessions[session_id]
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session info."""
        return self._sessions.get(session_id)
    
    def end_session(self, session_id: str) -> None:
        """End and cleanup a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
        claude_code_driver.cleanup_session(session_id)
    
    async def chat(
        self,
        message: str,
        session_id: str,
        continue_conversation: bool = True
    ) -> AsyncIterator[dict]:
        """
        Send a message and stream response.
        
        Args:
            message: User message
            session_id: Session ID
            continue_conversation: Whether to continue previous context
            
        Yields:
            Event dicts from Claude Code driver
        """
        # Ensure session exists
        if session_id not in self._sessions:
            self.start_session(session_id)
        
        self._sessions[session_id]["message_count"] += 1
        
        # Determine if we should continue
        should_continue = (
            continue_conversation and 
            self._sessions[session_id]["message_count"] > 1
        )
        
        async for event in claude_code_driver.execute(
            message=message,
            session_id=session_id,
            system_prompt=self.system_prompt,
            continue_conversation=should_continue,
            allowed_tools=self.allowed_tools,
        ):
            yield event
    
    async def chat_simple(
        self,
        message: str,
        session_id: str
    ) -> str:
        """
        Send message and get complete response.
        
        Non-streaming convenience method.
        """
        chunks = []
        async for event in self.chat(message, session_id):
            if event["type"] == "text":
                chunks.append(event["content"])
            elif event["type"] == "error":
                raise RuntimeError(event["message"])
        return "".join(chunks)


# Singleton instance
agent_service = AgentService()
