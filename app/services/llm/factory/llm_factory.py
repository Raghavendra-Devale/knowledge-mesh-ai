import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

from app.services.llm.providers.gemini_provider import GeminiProvider
from app.services.llm.providers.openai_provider import OpenAIProvider


class LLMFactory:

    @staticmethod
    def create():

        provider = settings.LLM_PROVIDER
        logger.info("Initializing LLM provider: %s", provider)

        if provider == "gemini":
            return GeminiProvider()

        if provider == "openai":
            return OpenAIProvider()

        logger.error("Unsupported LLM provider: %s", provider)
        raise ValueError("Unsupported LLM provider")