import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

from app.core.database import get_db
from app.core.dependencies import get_ingestion_service

from app.services.ingestion.ingestion_service import IngestionService


router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"]
)


@router.post("/pdf")
async def ingest_pdf(
    pdf_path: str,
    db: AsyncSession = Depends(get_db),
    ingestion_service: IngestionService = Depends(get_ingestion_service)
):
    logger.info(f"Received ingestion request for PDF: {pdf_path}")

    return await ingestion_service.ingest_pdf(
        db,
        pdf_path
    )