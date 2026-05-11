from app.repositories.conversation_repository import (
    ConversationRepository
)

from app.repositories.chat_message_repository import (
    ChatMessageRepository
)


class ChatService:

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        chat_message_repository: ChatMessageRepository
    ):

        self.conversation_repository = conversation_repository

        self.chat_message_repository = chat_message_repository

    async def create_conversation(
        self,
        user_id: str,
        title: str | None = None
    ):

        return await self.conversation_repository.create_conversation(
            user_id=user_id,
            title=title
        )

    async def save_user_message(
        self,
        conversation_id: int,
        user_id: str,
        content: str
    ):

        return await self.chat_message_repository.save_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=content
        )

    async def save_assistant_message(
        self,
        conversation_id: int,
        user_id: str,
        content: str
    ):

        return await self.chat_message_repository.save_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=content
        )

    async def get_recent_conversation_history(
        self,
        conversation_id: int,
        limit: int = 6
    ):

        return await self.chat_message_repository.get_recent_messages(
            conversation_id=conversation_id,
            limit=limit
        )