import httpx
from email.mime.text import MIMEText
from src.models.smtp_model import EmailRequest,EmailRequestO365
from src.interfaces.email_service import IEmailService
from src.config.config import settings
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import aiosmtplib
from O365 import Account, Message
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

class o365EmailService(IEmailService):
    def enviar_correo(request: EmailRequestO365):
        #configurando cuerpo del correo
        subject= request.subject
        body_html= request.body
        to=request.to
        cc=request.cc
        bcc=request.bcc
        adjuntos=request.adjuntos
        imagenes_embed=request.imagenes_embed

        #configurando varialbles de entorno
        tenant = settings.O365_TENANT_ID
        client_id = settings.O365_CLIENT_ID
        client_secret = settings.O365_CLIENT_SECRET
        username = settings.O365_USERNAME


        credentials = (client_id, client_secret)
        account = Account(credentials, auth_flow_type='credentials', tenant_id=tenant)
        account.authenticate()
        if account.authenticate():
            mailbox = account.mailbox(username)
            message = mailbox.new_message()
            message.to.add(to)
            if cc:
                message.cc.add(cc if isinstance(cc, list) else [cc])
            if bcc:
                message.bcc.add(bcc if isinstance(bcc, list) else [bcc])
            message.subject = subject
            message.body = body_html
            message.body_type =  "html"

            # Adjuntos
            if adjuntos:
                for adj in adjuntos:
                    message.attachments.add(Path(adj))

            # Imágenes embebidas
            if imagenes_embed:
                for cid, img_path in imagenes_embed.items():
                    message.attachments.add(Path(img_path), is_inline=True, cid=cid)

            message.send()
        else:
            print("Error de autenticación")



