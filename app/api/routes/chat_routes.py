import logging
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import json

logger = logging.getLogger(__name__)


from app.core.dependencies import get_rag_service
from app.services.rag_service import RagService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    message: str
    conversation_id: int
    user_id: Optional[str] = None


@router.post("/")
async def chat(
    request: ChatRequest,
    rag_service: RagService = Depends(get_rag_service)
):
    logger.info(f"Received chat request: {request.message} from user: {request.user_id}")

    response = await rag_service.ask(
        question=request.message,
        conversation_id=request.conversation_id,
        user_id=request.user_id
    )
    logger.info("Response:\n")
    logger.info(json.dumps(response, indent=4))
    return response