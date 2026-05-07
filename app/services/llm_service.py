from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.llm.llm_factory import get_llm_provider

from app.core.config import settings

class LLMService:
    def __init__(self):
        
        self.provider = get_llm_provider()
        
    async def generate_response(
        self,
        prompt:str
    ) -> str:
        
        return await self.provider.generate_response(
            prompt = prompt
        )