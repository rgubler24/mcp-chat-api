"""API routes"""

from fastapi import APIRouter
from app.api.routes import chat, api_keys

# Create main API router
api_router = APIRouter()

# Include route modules
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"])


