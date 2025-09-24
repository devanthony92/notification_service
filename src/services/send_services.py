
from src.config.config import settings
from fastapi.responses import JSONResponse 
from fastapi import HTTPException
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
        try:
            dataplantilla = self.db.query(Plantillas).filter(Plantillas.identifying_name == req.identifying_name).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Fallo la consulta a la base de datos", error = e)
        message = EmailMessage()
        message["From"] = self.user
        message["To"] = req.to
        message["Subject"] = req.subject
        message_body = dataplantilla.content_html if dataplantilla else req.body
        message.set_content(message_body)
        message.add_alternative(message_body, subtype="html")

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

    # Autenticación obligatoria
    def _autenticate(self):    
        if not self.account.is_authenticated:
             if not self.account.authenticate():
                  raise Exception("Error de autenticación con O365")

    async def send_email(self, request: EmailRequest) -> dict:           
            try:
                mailbox = self.account.mailbox(self.username)
                message = mailbox.new_message()
                try:
                    dataplantilla = self.db.query(Plantillas).filter(Plantillas.identifying_name == request.identifying_name).first()
                except Exception as e:
                    raise HTTPException(status_code=500, detail="Fallo la consulta a la base de datos", error = e)
                message.to.add(request.to)
                if request.cc:
                    message.cc.add(request.cc if isinstance(request.cc, list) else [request.cc])
                if request.bcc:
                    message.bcc.add(request.bcc if isinstance(request.bcc, list) else [request.bcc])
                message.subject = request.subject
                #message.body = request.body
                message.body = dataplantilla.content_html if dataplantilla else request.body
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
            except Exception as e:
                return JSONResponse(
                    content={
                        "status": str(e),
                        "message": "No se pudo realizar el envio del Email",
                        "data": request,
                    },
                    status_code=500,
                )



