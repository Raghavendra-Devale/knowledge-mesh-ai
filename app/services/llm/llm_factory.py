from app.core.config import settings
from app.services.llm.gemini_provider import GeminiProvider
from app.services.llm.openai_provider import OpenAIProvider

def get_llm_provider():
    
    if settings.LLM_PROVIDER == "openai":
        return OpenAIProvider()
    return GeminiProvider()