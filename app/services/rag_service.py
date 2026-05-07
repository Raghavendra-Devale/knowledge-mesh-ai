from app.services.retrieval.retrieval_service import RetrievalService
from app.services.llm_service import LLMService


class RagService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: LLMService
    ):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service


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

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say you do not have enough information.

Context:
{context}

Question:
{question}
"""

        answer = await self.llm_service.generate_response(
            prompt=prompt
        )

        return {
            "question": question,
            "answer": answer,
            # "sources": [
            #         {
            #             "content": chunk.content,
            #             "document_name": chunk.document_name,
            #             "page_number": chunk.page_number,
            #             "source_type": chunk.source_type,
            #             "source_url": chunk.source_url
            #         }
            #         for chunk in chunks
            #     ]
        }