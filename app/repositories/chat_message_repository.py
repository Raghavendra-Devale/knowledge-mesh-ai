from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import ChatMessage


class ChatMessageRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_message(
        self,
        conversation_id: int,
        user_id: str,
        role: str,
        content: str
    ) -> ChatMessage:

        message = ChatMessage(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )

        self.db.add(message)

        await self.db.commit()

        await self.db.refresh(message)

        return message

    async def get_recent_messages(
        self,
        conversation_id: int,
        limit: int = 6
    ) -> list[ChatMessage]:

        result = await self.db.execute(
            select(ChatMessage)
            .where(
                ChatMessage.conversation_id == conversation_id
            )
            .order_by(desc(ChatMessage.created_at))
            .limit(limit)
        )

        messages = result.scalars().all()

        return list(reversed(messages))

    async def get_today_messages(
        self,
        user_id: str,
        conversation_id: int,
        limit: int = 10
    ) -> list[ChatMessage]:

        result = await self.db.execute(
            select(ChatMessage)
            .where(
                ChatMessage.user_id == user_id,
                ChatMessage.conversation_id == conversation_id,
                func.date(ChatMessage.created_at) == func.current_date()
            )
            .order_by(desc(ChatMessage.created_at))
            .limit(limit)
        )

        messages = result.scalars().all()

        return list(reversed(messages))