from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import get_rag_service
from app.services.rag_service import RagService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    question: str


@router.post("/")
async def chat(
    request: ChatRequest,
    rag_service: RagService = Depends(get_rag_service)
):

    response = await rag_service.ask(
        question=request.question
    )

    return response