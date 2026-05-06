from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding_service import EmbeddingService


class RetrievalService:

    def __init__(
        self,
        chunk_repository: ChunkRepository,
        embedding_service: EmbeddingService
    ):

        self.chunk_repository = chunk_repository
        self.embedding_service = embedding_service


    async def retrieve(
        self,
        question: str,
        limit: int = 5
    ):

        query_embedding = self.embedding_service.generate_embedding(
            question
        )

        chunks = await self.chunk_repository.search_similar_chunks(
            query_embedding=query_embedding,
            limit=limit
        )

        return chunks