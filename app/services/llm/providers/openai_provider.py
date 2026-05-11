import logging
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.services.llm.llm_provider import LLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):

    def __init__(self):

        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.3
        )

    async def generate(self, full_prompt: str) -> str:
        logger.info("Generating response with OpenAI model.")
        response = await self.llm.ainvoke(full_prompt)

        return response.content