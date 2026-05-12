import logging
import uuid

from app.services.retrieval.retrieval_service import RetrievalService
from app.services.llm.llm_provider import LLMProvider
from app.services.chat_service import ChatService
from typing import Optional


logger = logging.getLogger(__name__)


class RagService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_provider: LLMProvider,
        chat_service: ChatService
    ):

        self.retrieval_service = retrieval_service
        self.llm_provider = llm_provider
        self.chat_service = chat_service

    async def ask(
        self,
        question: str,
        conversation_id: Optional[int] = None,
        user_id: Optional[str] = None
    ):

        logger.info(
            "Received Ask Request - Conversation ID: %s, User ID: %s",
            conversation_id,
            user_id
        )

        if user_id:
            try:
                uuid.UUID(user_id)
            except ValueError:
                user_id = None

        if not user_id:

            logger.info("User ID is None, generating new user_id")

            user_id = str(uuid.uuid4())

            logger.info("New User ID: %s", user_id)

        if not conversation_id:
            conversation = await self.chat_service.create_conversation(user_id=user_id)
            conversation_id = conversation.id

        await self.chat_service.save_user_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content=question
        )

        # STEP 1 — Load today's conversation history
        history = await self.chat_service.get_today_conversation_history(
            user_id=user_id,
            conversation_id=conversation_id
        )

        logger.info("User ID: %s", user_id)
        logger.info("History Count: %d", len(history))

        # STEP 2 — Format conversation history
        conversation_context = self.format_conversation_history(
            history
        )

        # STEP 3 — Rewrite query for better retrieval
        rewritten_query = await self.rewrite_query(
            conversation_history=conversation_context,
            question=question
        )

        logger.info(
            "Rewritten Query: %s",
            rewritten_query
        )

        # STEP 4 — Retrieve relevant chunks
        retrieval_response = await self.retrieval_service.retrieve(
            question=rewritten_query,
            limit=5
        )

        # STEP 5 — Handle empty retrieval
        if not retrieval_response.results:

            return {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "reply": (
                    "I couldn't find any relevant "
                    "information in the documents."
                ),
                "sources": []
            }

        # STEP 6 — Build retrieval context
        context = "\n\n".join(
            result.content
            for result in retrieval_response.results
        )

        logger.info(
            "Retrieved Context: %s",
            context
        )

        # STEP 8 — Build final prompt
        full_prompt = f"""
You are a helpful AI assistant.

Conversation History:
{conversation_context}

Retrieved Context:
{context}

Current User Question:
{question}

Instructions:
- Answer ONLY using the retrieved context.
- If information is missing, clearly say so.
- Keep the answer concise and accurate.
"""

        # STEP 9 — Generate final answer
        answer = await self.llm_provider.generate(
            full_prompt=full_prompt
        )

        logger.info(
            "Generated Answer: %s",
            answer
        )

        # STEP 10 — Save assistant response
        await self.chat_service.save_assistant_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content=answer
        )

        # STEP 11 — Return response
        return {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "reply": answer,
            "sources": [
                {
                    "content": result.content,
                    "document_name": result.metadata.get(
                        "document_name"
                    ),
                    "page_number": result.metadata.get(
                        "page_number"
                    ),
                    "source_type": result.metadata.get(
                        "source_type"
                    ),
                    "source_url": result.metadata.get(
                        "source_url"
                    ),
                    "similarity_score": result.similarity_score
                }
                for result in retrieval_response.results
            ]
        }

    async def rewrite_query(
        self,
        conversation_history: str,
        question: str
    ) -> str:

        # No history → no rewrite needed
        if not conversation_history.strip():
            return question

        rewrite_prompt = f"""
Rewrite the user's latest question into a clear standalone search query.

Conversation History:
{conversation_history}

Current User Question:
{question}

Standalone Search Query:
"""

        rewritten_query = await self.llm_provider.generate(
            full_prompt=rewrite_prompt
        )

        return rewritten_query.strip()

    def format_conversation_history(
        self,
        messages
    ) -> str:

        if not messages:
            return ""

        formatted_messages = []

        for message in messages:

            formatted_messages.append(
                f"{message.role.capitalize()}: "
                f"{message.content}"
            )

        return "\n".join(formatted_messages)