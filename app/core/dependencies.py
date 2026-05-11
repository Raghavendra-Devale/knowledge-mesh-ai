from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.repositories.chunk_repository import ChunkRepository

from app.services.embedding_service import EmbeddingService
from app.services.retrieval.retrieval_service import RetrievalService
from app.services.llm.llm_provider import LLMProvider
from app.services.llm.llm_factory import LLMFactory
from app.services.chat_service import ChatService
from app.services.rag_service import RagService

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.chat_message_repository import ChatMessageRepository

from app.services.ingestion.ingestion_service import IngestionService
from app.services.chunking_service import ChunkingService



def get_chunk_repository(
    db: AsyncSession = Depends(get_db)
):
    return ChunkRepository(db)


def get_embedding_service(
    request: Request
):
    return request.app.state.embedding_service


def get_retrieval_service(
    chunk_repository: ChunkRepository = Depends(get_chunk_repository),
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):

    return RetrievalService(
        chunk_repository=chunk_repository,
        embedding_service=embedding_service
    )


def get_llm_provider():
    return LLMFactory.create()


def get_conversation_repository(db: AsyncSession = Depends(get_db)):
    return ConversationRepository(db)

def get_chat_message_repository(db: AsyncSession = Depends(get_db)):
    return ChatMessageRepository(db)

def get_chat_service(
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
    chat_message_repository: ChatMessageRepository = Depends(get_chat_message_repository)
):
    return ChatService(
        conversation_repository=conversation_repository,
        chat_message_repository=chat_message_repository
    )

def get_rag_service(
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
    llm_provider: LLMProvider = Depends(get_llm_provider),
    chat_service: ChatService = Depends(get_chat_service)
):

    return RagService(
        retrieval_service=retrieval_service,
        llm_provider=llm_provider,
        chat_service=chat_service
    )

def get_chunking_service():
    return ChunkingService()


def get_ingestion_service(
    chunk_repository: ChunkRepository = Depends(get_chunk_repository),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    chunking_service: ChunkingService = Depends(get_chunking_service)
):

    return IngestionService(
        chunk_repository=chunk_repository,
        embedding_service=embedding_service,
        chunking_service=chunking_service
    )