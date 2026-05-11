from app.core.config import settings

from app.services.llm.providers.gemini_provider import GeminiProvider
from app.services.llm.providers.openai_provider import OpenAIProvider


class LLMFactory:

    @staticmethod
    def create():

        provider = settings.LLM_PROVIDER

        if provider == "gemini":
            return GeminiProvider()

        if provider == "openai":
            return OpenAIProvider()

        raise ValueError("Unsupported LLM provider")