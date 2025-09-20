from fastapi import APIRouter, HTTPException
from src.models.smtp_model import EmailRequest
from config.config import settings
from httpx import AsyncClient

router = APIRouter(prefix="/emails",tags=["Emails"])

SERVICES = {
    "smtp" : settings.SMTP_URL,
    "o365" : settings.O365_URL,
}

@router.post("/send/{provider}")
async def send_email(provider: str, req: EmailRequest):
    if provider not in SERVICES:
        raise HTTPException(status_code=400, detail="Proveedor no soportado")
    
    URL = SERVICES[provider]
    async with AsyncClient() as http_client:
        response = await http_client.post(URL, json=req.dict())
        return response.json()