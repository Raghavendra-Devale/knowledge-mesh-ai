from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.services.llm.llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):

    def __init__(self):

        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.3
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