# Conversational Identity & User ID Implementation

This document explains the flow and implementation of the conversational identity mechanism (via `user_id`) in the application. The goal is to provide a seamless conversational memory that persists across multiple requests from the same user while ensuring security and robustness.

## 1. Optional `user_id` in the API Request

In `app/api/routes/chat_routes.py`, the `ChatRequest` model defines `user_id` as an optional parameter:

```python
class ChatRequest(BaseModel):
    message: str
    conversation_id: int
    user_id: Optional[str] = None
```

When a frontend client initiates a conversation for the first time, it does not have a `user_id`, so it sends a request without one. For subsequent requests, the frontend sends back the `user_id` it received from the backend.

## 2. UUID Validation & Generation

Inside `app/services/rag_service.py`, the `ask` method receives the `user_id`. The backend is the authoritative source for user identity, so it must validate the incoming string.

```python
if user_id:
    try:
        # Validate that the provided user_id is a valid UUID
        uuid.UUID(user_id)
    except ValueError:
        # If invalid (e.g. "raghav", "null", or ""), discard it
        user_id = None

if not user_id:
    # Generate a fresh UUID for new users or invalid identities
    user_id = str(uuid.uuid4())
```

This ensures that any malformed strings or placeholder values (like `"null"` from JavaScript `localStorage`) are rejected, and a new valid UUID is securely generated.

## 3. Saving the Message & Loading Today's History

Once the `user_id` is validated (or generated), the system saves the user's message using `chat_service.save_user_message`.

After saving the current message, the system loads the conversation history:

```python
history = await self.chat_service.get_today_conversation_history(user_id=user_id)
```

In `app/repositories/chat_message_repository.py`, this query filters messages by the `user_id` and explicitly limits the results to **today's date**:

```python
result = await self.db.execute(
    select(ChatMessage)
    .where(
        ChatMessage.user_id == user_id,
        func.date(ChatMessage.created_at) == func.current_date()
    )
    .order_by(desc(ChatMessage.created_at))
    .limit(limit)
)
```

This guarantees that old chats from previous days do not pollute the current conversational context.

## 4. Returning the Identity to the Frontend

After retrieving the context and generating an answer via the LLM, the backend returns the response:

```python
return {
    "user_id": user_id,
    "reply": answer,
    "sources": [...]
}
```

If a new `user_id` was generated in Step 2, the frontend now receives it. The frontend should save this `user_id` (e.g. in cookies or `localStorage`) and include it in all future requests to maintain conversational memory.
