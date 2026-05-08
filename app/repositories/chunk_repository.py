from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
            select(DocumentChunk)
            .order_by(
                DocumentChunk.embedding.cosine_distance(query_embedding)
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()
    
    
    
    async def save_chunks(self, chunks: list):
        print(f"Saving {len(chunks)} chunks to database")

        self.db.add_all(chunks)
        await self.db.commit()
        print("Chunks committed successfully")