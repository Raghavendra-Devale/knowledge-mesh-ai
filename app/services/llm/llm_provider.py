from abc import ABC, abstractmethod

class LLMProvider(ABC):
    
    @abstractmethod
    async def generate(self, full_prompt: str) -> str:
        pass
