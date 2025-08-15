from fastapi import APIRouter
from .chat import router as chat_router
from .chat_simple import router as chat_simple_router

router = APIRouter()

router.include_router(chat_router, tags=["chat"])
router.include_router(chat_simple_router, tags=["chat-simple"])
