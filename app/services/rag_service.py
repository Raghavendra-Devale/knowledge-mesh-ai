from app.services.retrieval.retrieval_service import RetrievalService
from app.services.llm.llm_provider import LLMProvider


class RagService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_provider: LLMProvider
    ):
        self.retrieval_service = retrieval_service
        self.llm_provider = llm_provider


    async def ask(
        self,
        question: str
    ):

        chunks = await self.retrieval_service.retrieve(
            question=question,
            limit=5
        )

        context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        answer = await self.llm_provider.generate(
            prompt=question,
            context=context
        )

        return {
        "reply": answer,
        "sources": [
            {
                "content": chunk.content,
                "document_name": chunk.document_name,
                "page_number": chunk.page_number,
                "source_type": chunk.source_type,
                "source_url": chunk.source_url
            }
            for chunk in chunks
        ]
    }