
from src.interfaces.email_service import IEmailService
from src.config.config import settings
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import aiosmtplib, asyncio
from O365 import Account
from pathlib import Path
from sqlalchemy.orm import Session
from src.models.smtp_model import EmailRequest,EmailRequest
from src.models.template_model  import Plantillas

class SmtpEmailService:
#Servicio para enviar correos usando SMTP clásico (asincrónico con aiosmtplib).

    def __init__(self, db: Session):
         self.db = db
         self.host = settings.SMTP_SERVER
         self.port = settings.SMTP_PORT
         self.user = settings.SMTP_USER
         self.password = settings.SMTP_PASS

    async def send(self, req: EmailRequest) -> dict:
        message = EmailMessage()
        message["From"] = self.user
        message["To"] = req.to
        message["Subject"] = req.subject
        message.set_content(req.body)
        message.add_alternative(req.body, subtype="html")

        try:
            await   aiosmtplib.send(
                    message,
                    hostname = self.host,
                    port = self.port,
                    username = self.user,
                    password = self.password,
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

class O365EmailService:
#Servicio para enviar correos usando o365 (asincrónico).

    def __init__(self, db: Session):
        self.db = db
        self.username = settings.O365_USERNAME
        self._init_account()

    def _init_account(self):
        credentials = (settings.O365_CLIENT_ID, settings.O365_CLIENT_SECRET)
        self.account = Account(
            credentials=credentials,
            auth_flow_type="credentials",
            tenant_id=settings.O365_TENANT_ID
        )
        self._autenticate()

    # Autenticación obligatoria (bloqueante, la envolvemos en hilo)
    def _autenticate(self):    
        if not self.account.is_authenticated:
             if not self.account.authenticate():
                  raise Exception("Error de autenticación con O365")

    async def send_email(self, request: EmailRequest) -> dict:           

                mailbox = self.account.mailbox(self.username)
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



