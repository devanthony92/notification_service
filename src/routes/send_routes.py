# Módulo de rutas para el envío de correos electrónicos vía SMTP.
# exponemos el endpoint para enviar correos de forma asíncrona

# dependencias y paqueterias utilizadas en el desarrollo del modulo de notificaciones
from fastapi import APIRouter, HTTPException, Depends
from src.models.smtp_model import EmailRequest, EmailRequestO365
from src.services.send_services import SmtpEmailService,O365EmailService
from sqlalchemy.orm import Session
from src.config.config  import get_session

# inicializacion del roter 
sendemail_routes = APIRouter()

# Este endpoint permite enviar correos electrónicos mediante el servicio SMTP.
# La tarea de envío se ejecuta en segundo plano utilizando `BackgroundTasks`,
# lo cual asegura una respuesta rápida al cliente sin necesidad de esperar
# que el correo se envíe completamente.

@sendemail_routes.post("/sendSMTP")
async def send_email_smtp(request: EmailRequest, db: Session = Depends(get_session)):
    # Endpoint para enviar un correo usando SMTP.
    try:
        result = await SmtpEmailService(db).send(request)
        return {"message": "Correo enviado correctamente", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando correo: {str(e)}")

@sendemail_routes.post("/sendO365")
async def send_email_o365(request: EmailRequestO365, db: Session = Depends(get_session)):
    # Endpoint para enviar un correo usando O365.
    try:
        result = await O365EmailService(db).send(request)
        return {"message": "Correo enviado correctamente", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    