"""
API Router - aggregates all API routes
"""
from fastapi import APIRouter

api_router = APIRouter()


# Health check
@api_router.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"message": "pong"}


# Chat routes (Agent interaction)
from src.modules.chat.router import router as chat_router
api_router.include_router(chat_router, tags=["chat"])


# Example: Include other module routers
# from src.modules.user.api import router as user_router
# api_router.include_router(user_router, prefix="/users", tags=["users"])
