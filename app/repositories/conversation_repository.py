from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import Conversation


class ConversationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(
        self,
        user_id: str,
        title: str | None = None
    ) -> Conversation:

        conversation = Conversation(
            user_id=user_id,
            title=title
        )

        self.db.add(conversation)

        await self.db.commit()

        await self.db.refresh(conversation)

        return conversation

    async def get_conversation_by_id(
        self,
        conversation_id: int
    ) -> Conversation | None:

        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id
            )
        )

        return result.scalar_one_or_none()