import logging
from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

from app.models.retrieval import (
    RetrievalResult,
    RetrievalResponse
)


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
    ) -> RetrievalResponse:
        logger.info("=" * 80)
        logger.info("USER QUESTION:")
        logger.info(question)

        cleaned_question = self.preprocess_query(
            question
        )

        query_embedding = self.embedding_service.generate_embedding(
            cleaned_question
        )

        logger.info(
            f"Query embedding dimensions: {len(query_embedding)}"
        )

        # Semantic Retrieval
        retrieved_chunks = await self.chunk_repository.search_similar_chunks(
            query_embedding=query_embedding,
            limit=limit
        )

        # Keyword Retrieval
        keyword_chunks = await self.chunk_repository.search_keyword_chunks(
            question=cleaned_question,
            limit=limit
        )

        logger.info(
            f"Semantic chunks count: {len(retrieved_chunks)}"
        )

        logger.info(
            f"Keyword chunks count: {len(keyword_chunks)}"
        )

        results = []

        seen_chunk_ids = set()

        distance_threshold = 0.45

        # Process Semantic Results
        for index, (chunk, distance) in enumerate(retrieved_chunks):

            if distance > distance_threshold:

                logger.info(
                    f"Skipping weak semantic chunk "
                    f"with distance {distance}"
                )

                continue

            logger.info("=" * 80)
            logger.info(
                f"Retrieved Semantic Chunk {index + 1}"
            )
            logger.info(f"Distance Score: {distance}")
            logger.info("=" * 80)

            result = RetrievalResult(
                chunk_id=chunk.id,
                content=chunk.content,
                similarity_score=float(distance),
                metadata={
                    "document_name": chunk.document_name,
                    "page_number": chunk.page_number,
                    "source_type": chunk.source_type,
                    "source_url": chunk.source_url,
                    "chunk_index": chunk.chunk_index,
                    "retrieval_method": "semantic"
                },
                retrieval_source="semantic"
            )

            results.append(result)

            seen_chunk_ids.add(chunk.id)

        # Process Keyword Results
        for chunk, rank in keyword_chunks:

            if chunk.id in seen_chunk_ids:
                continue

            logger.info("=" * 80)
            logger.info("Retrieved Keyword Chunk")
            logger.info("=" * 80)

            result = RetrievalResult(
                chunk_id=chunk.id,
                content=chunk.content,
                similarity_score=float(rank),
                metadata={
                    "document_name": chunk.document_name,
                    "page_number": chunk.page_number,
                    "source_type": chunk.source_type,
                    "source_url": chunk.source_url,
                    "chunk_index": chunk.chunk_index,
                    "retrieval_method": "keyword"
                },
                retrieval_source="keyword"
            )

            results.append(result)

            seen_chunk_ids.add(chunk.id)

        return RetrievalResponse(
            query=cleaned_question,
            results=results
        )
    
    def preprocess_query(
        self,
        question: str
    ) -> str:

        stop_words = {
            "find",
            "show",
            "give",
            "tell",
            "details",
            "information",
            "about",
            "please",
            "me"
        }

        words = question.lower().split()

        cleaned_words = [
            word
            for word in words
            if word not in stop_words
        ]

        cleaned_query = " ".join(cleaned_words)

        logger.info(
            f"Cleaned Query: {cleaned_query}"
        )

        return cleaned_query
