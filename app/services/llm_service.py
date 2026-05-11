from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.llm.factory.llm_factory import get_llm_provider

from app.core.config import settings

class LLMService:

    def __init__(self):

        self.provider = get_llm_provider()

    async def generate_response(
        self,
        prompt: str
    ) -> str:

        return await self.provider.generate_response(
            prompt=prompt
        )

    async def rewrite_query(
        self,
        conversation_history: str,
        question: str
    ) -> str:

        prompt = f"""
Rewrite the user's latest question into a clear standalone search query.

Conversation History:
{conversation_history}

Current User Question:
{question}

Standalone Search Query:
"""

        return await self.provider.generate_response(
            prompt=prompt
        )