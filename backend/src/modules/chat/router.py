"""
Chat API Routes

Handles chat interactions with the agent via SSE streaming.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
import uuid

from ..agent.service import agent_service


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Chat request payload."""
    message: str
    session_id: Optional[str] = None


class SessionResponse(BaseModel):
    """Session info response."""
    session_id: str
    message_count: int


@router.post("/sessions")
async def create_session() -> SessionResponse:
    """Create a new chat session."""
    session_id = str(uuid.uuid4())
    session = agent_service.start_session(session_id)
    return SessionResponse(
        session_id=session_id,
        message_count=0
    )


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """End and cleanup a chat session."""
    agent_service.end_session(session_id)
    return {"status": "ok"}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str) -> SessionResponse:
    """Get session info."""
    session = agent_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionResponse(
        session_id=session["id"],
        message_count=session["message_count"]
    )


@router.post("/message")
async def send_message(request: ChatRequest):
    """
    Send a message and stream response via SSE.
    
    Returns Server-Sent Events stream with events:
    - event: text, data: {"content": "..."}
    - event: tool_use, data: {"tool": "...", "input": {...}}
    - event: tool_result, data: {"tool": "...", "output": "..."}
    - event: error, data: {"message": "..."}
    - event: done, data: {}
    """
    session_id = request.session_id or str(uuid.uuid4())
    
    async def event_generator():
        try:
            async for event in agent_service.chat(
                message=request.message,
                session_id=session_id
            ):
                event_type = event.get("type", "text")
                data = json.dumps(event)
                yield f"event: {event_type}\ndata: {data}\n\n"
        except Exception as e:
            error_data = json.dumps({"type": "error", "message": str(e)})
            yield f"event: error\ndata: {error_data}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-Id": session_id,
        }
    )


@router.post("/message/sync")
async def send_message_sync(request: ChatRequest):
    """
    Send a message and wait for complete response.
    
    Non-streaming alternative for simple use cases.
    """
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        response = await agent_service.chat_simple(
            message=request.message,
            session_id=session_id
        )
        return {
            "session_id": session_id,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Admin Routes (optional - for management)
# ============================================

@router.post("/admin/reload-prompt")
async def reload_prompt():
    """Reload system prompt from file."""
    agent_service.reload_prompt()
    return {"status": "ok", "message": "Prompt reloaded"}


@router.post("/admin/set-persona")
async def set_persona(persona: str):
    """Switch agent persona."""
    agent_service.set_persona(persona)
    return {"status": "ok", "persona": persona}
