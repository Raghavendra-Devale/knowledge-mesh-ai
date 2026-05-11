from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.llm.llm_provider import LLMProvider

class GeminiProvider(LLMProvider):
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            temperature = 0.3            
        )
        
    async def generate(self, prompt: str, context: str) -> str:
        full_prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say you do not have enough information.

Context:
{context}

Question:
{prompt}
"""
        response = await self.llm.ainvoke(full_prompt)
        return response.content    