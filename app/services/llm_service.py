from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

class LLMService:
    def __init__(self):
        
        self.llm = ChatGoogleGenerativeAI(
            model = settings.GEMINI_MODEL,
            google_api_key = settings.GEMINI_API_KEY,
            temperature = 0.3
        )
        
    async def generate_answer(
        self,
        prompt:str
    ) -> str:
        
        response = await self.llm.ainvoke(prompt)
        
        return response.content