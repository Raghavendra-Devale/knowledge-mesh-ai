import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

from app.services.llm.providers.gemini_provider import GeminiProvider
from app.services.llm.providers.openai_provider import OpenAIProvider


class LLMFactory:

    @staticmethod
    def create():

        provider = settings.LLM_PROVIDER
        logger.info(f"Initializing LLM provider: {provider}")

        if provider == "gemini":
            return GeminiProvider()

        if provider == "openai":
            return OpenAIProvider()

        logger.error(f"Unsupported LLM provider: {provider}")
        raise ValueError("Unsupported LLM provider")