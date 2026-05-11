import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.llm.llm_provider import LLMProvider
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiProvider(LLMProvider):
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=settings.GEMINI_API_KEY,
            temperature=0.3            
        )
        
    async def generate(self, full_prompt: str) -> str:
        logger.info("Generating response with Gemini model.")
        response = await self.llm.ainvoke(full_prompt)
        return response.content    