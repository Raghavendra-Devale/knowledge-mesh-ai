import logging
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        logger.info("Initializing EmbeddingService...")
        self.model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        logger.info("EmbeddingService initialized successfully")
    
    def generate_embedding(self, text: str):
        
        logger.info("Generating embedding for text length: %d", len(text))

        return self.model.embed_query(text)
    
    