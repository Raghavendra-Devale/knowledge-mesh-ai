from app.api.routes.ingestion_routes import router as ingestion_router
from app.api.routes.chat_routes import router as chat_router

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.services.embedding_service import EmbeddingService


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading embedding model...")

    app.state.embedding_service = EmbeddingService()

    yield

    print("Shutting down application...")
    

app = FastAPI(
    lifespan=lifespan
)

app.include_router(ingestion_router)

app.include_router(chat_router)

@app.get("/")
def health():
    return{"status": "running"} 
