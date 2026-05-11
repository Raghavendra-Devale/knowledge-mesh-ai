import logging
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.ingestion_routes import router as ingestion_router
from app.api.routes.chat_routes import router as chat_router

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.services.embedding_service import EmbeddingService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Loading embedding model...")

    app.state.embedding_service = EmbeddingService()

    yield

    logger.info("Shutting down application...")
    

app = FastAPI(
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion_router)

app.include_router(chat_router)

@app.get("/")
def health():
    return{"status": "running"} 
