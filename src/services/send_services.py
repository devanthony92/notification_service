from src.models.smtp_model import EmailRequest,EmailRequestO365
from src.interfaces.email_service import IEmailService
from src.config.config import settings
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import aiosmtplib, asyncio
from O365 import Account
from pathlib import Path

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
                    hostname = settings.SMTP_SERVER,
                    port = settings.SMTP_PORT,
                    username = settings.SMTP_USER,
                    password = settings.SMTP_PASS,
                    start_tls= True
            )
            return JSONResponse(
                    content={
                            "status": "success",
                            "message": f"Correo enviado a {req.to}",
                            "subject": req.subject,
                    },
                    status_code=200,
                    )
            
        except aiosmtplib.errors as e:
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

class O365EmailService(IEmailService):
    async def send_email(request: EmailRequestO365) -> None:           
            #configurando varialbles de entorno
            tenant = settings.O365_TENANT_ID
            client_id = settings.O365_CLIENT_ID
            client_secret = settings.O365_CLIENT_SECRET
            username = settings.O365_USERNAME

            credentials = (client_id, client_secret)
            account = Account(credentials, auth_flow_type='credentials', tenant_id=tenant)
            id_verificated =  await asyncio.to_thread(account.authenticate)
            if id_verificated:
                mailbox = account.mailbox(username)
                message = mailbox.new_message()
                message.to.add(request.to)
                if request.cc:
                    message.cc.add(request.cc if isinstance(request.cc, list) else [request.cc])
                if request.bcc:
                    message.bcc.add(request.bcc if isinstance(request.bcc, list) else [request.bcc])
                message.subject = request.subject
                message.body = request.body
                message.body_type =  "html"

                # Adjuntos
                if request.adjuntos:
                    for adj in request.adjuntos:
                        message.attachments.add(Path(adj))

                # Imágenes embebidas
                if request.imagenes_embed:
                    for cid, img_path in request.imagenes_embed.items():
                        message.attachments.add(Path(img_path), is_inline=True, cid=cid)

                await asyncio.to_thread(message.send)
            else:
                print("Error de autenticación")



