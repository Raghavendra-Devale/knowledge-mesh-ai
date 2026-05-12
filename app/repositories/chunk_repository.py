import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)

from app.models.entities import DocumentChunk

class ChunkRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db


    async def search_similar_chunks(
        self,
        query_embedding: list[float],
        limit: int = 5
    ):

        stmt = (
            select(DocumentChunk,DocumentChunk.embedding.cosine_distance(query_embedding))
            .order_by(
                DocumentChunk.embedding.cosine_distance(query_embedding)
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return [(chunk,distance) for chunk, distance in result.all()]
    
    
    
    async def save_chunks(self, chunks: list):
        logger.info("Saving %d chunks to database", len(chunks))

        self.db.add_all(chunks)
        await self.db.commit()
        logger.info("Chunks committed successfully")


    async def search_keyword_chunks(
        self,
        question: str,
        limit: int = 5
    ):
        ts_query = func.plainto_tsquery(
            "english",
            question
        )
        stmt = (
            select(
                DocumentChunk,
                func.ts_rank(
                    DocumentChunk.search_vector,
                    ts_query
                ).label("rank")
            )
            .where(
                DocumentChunk.search_vector.op("@@")(ts_query)
            )
            .order_by(
                func.ts_rank(
                    DocumentChunk.search_vector,
                    ts_query
                ).desc()
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return [
            (chunk, rank)
            for chunk, rank in result.all()
        ]