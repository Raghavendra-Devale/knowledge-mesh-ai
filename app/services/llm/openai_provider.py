from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.services.llm.base_llm import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):

    def __init__(self):

        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.3
        )

    async def generate_response(
        self,
        prompt: str
    ) -> str:

        response = await self.llm.ainvoke(prompt)

        return response.content