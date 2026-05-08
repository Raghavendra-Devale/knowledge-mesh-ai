from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingService:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    
    def generate_embedding(self, text: str):
        
        print(f"Generating embedding for text length: {len(text)}")

        return self.model.embed_query(text)
    
    