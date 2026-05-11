from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.repositories.chunk_repository import ChunkRepository

from app.services.embedding_service import EmbeddingService
from app.services.retrieval.retrieval_service import RetrievalService
from app.services.llm.llm_provider import LLMProvider
from app.services.llm.llm_factory import LLMFactory
from app.services.rag_service import RagService


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


def get_rag_service(
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
    llm_provider: LLMProvider = Depends(get_llm_provider)
):

    return RagService(
        retrieval_service=retrieval_service,
        llm_provider=llm_provider
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