from langchain_community.document_loaders import PyPDFLoader

from app.models.entities import DocumentChunk
from app.repositories.chunk_repository import ChunkRepository
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService

from app.services.chunking_service import ChunkingService

import os


class IngestionService:
    
    def __init__(
        self,
        chunk_repository: ChunkRepository,
        embedding_service: EmbeddingService,
        chunking_service: ChunkingService
    ):
        self.chunk_repository = chunk_repository
        self.embedding_service = embedding_service
        self.chunking_service = chunking_service
        
    async def ingest_pdf(self, db, pdf_path: str):
        # pdf_path = r"C:/Users/devale/Downloads/Raghavendra_Devale (1).pdf"
        # print(os.path.exists(pdf_path))
        # print(os.path.isfile(pdf_path))
        
        loader = PyPDFLoader(pdf_path)
        print(repr(pdf_path))
        
        documents = loader.load()
        print(f"Pages loaded: {len(documents)}")

        chunks = self.chunking_service.split_text(documents)
       # logger.info(f"Total chunks created: {len(chunks)}")
        print(f"Total chunks created: {len(chunks)}")
        
        entities = []
        
        for index, chunk in enumerate(chunks):
            
            print(f"Chunk {index}:")
            print(chunk.page_content[:300])
            
            embedding = self.embedding_service.generate_embedding(
                chunk.page_content
            )
            
            entity = DocumentChunk(
                document_name = pdf_path.split("/")[-1],
                chunk_index = index,
                content = chunk.page_content,
                embedding = embedding
            )
            
            entities.append(entity)
        await self.chunk_repository.save_chunks(entities)
        
        return {
            "chunks_created": len(entities)
            
        }