from fastapi import APIRouter
from logging_config import get_logger


router = APIRouter()

logger = get_logger(__name__)


@router.get("/")
async def home():

    logger.info("Home endpoint called")

    return {"message": "Hello World"}


