from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.llm.base_llm import BaseLLMProvider

class GeminiProvider(BaseLLMProvider):
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            temperature = 0.3            
        )
        
    async def generate_response(self, prompt: str) -> str:
        response = await self.llm.ainvoke(prompt)
        return response.content
    