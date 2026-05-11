from fastapi import APIRouter, Depends
from pydantic import BaseModel
import json


from app.core.dependencies import get_rag_service
from app.services.rag_service import RagService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(
    request: ChatRequest,
    rag_service: RagService = Depends(get_rag_service)
):

    response = await rag_service.ask(
        question=request.message
    )
    print("Response:\n")
    print(json.dumps(response, indent=4))
    return response