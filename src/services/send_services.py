import httpx
from src.models.smtp_model import EmailRequest
from src.interfaces.email_service import IEmailService
from src.config.config import settings
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import aiosmtplib
#import smtplib

class SmtpEmailService(IEmailService):
    async def send(req: EmailRequest) -> None:
        try:
            message = EmailMessage()
            message["From"] = settings.EMAIL_FROM
            message["To"] = req.to
            message["Subject"] = req.subject
            message.set_content(req.body)

            await   aiosmtplib.send(
                    message,
                    hostname= settings.SMTP_SERVER,
                    port= settings.SMTP_PORT,
                    username= settings.SMTP_USER,
                    password= settings.SMTP_PASS,
                    start_tls=True
            )
            return JSONResponse(
                    content={
                            "status": "success",
                            "message": f"Correo enviado a {req.to}",
                            "subject": req.subject,
                    },
                    status_code=200,
                    )
            
        except httpx.HTTPStatusError as e:
               #manejo de error del envio
               return JSONResponse(
                 content={
                     "status": "error",
                     "message": str(e),
                     "to": req.to,
                     "subject": req.subject,
                 },
                 status_code=500,
               )

                 

                



