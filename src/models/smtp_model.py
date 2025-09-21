from pydantic import BaseModel, EmailStr
from typing import List, Optional

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str
    is_html: bool = False

class EmailRequestO365(BaseModel):
    subject: str
    body: str
    to: EmailStr
    cc: Optional[EmailStr] = None        #con copia al email
    bcc: Optional[EmailStr] = None       #con copia oculta al email
    adjuntos: Optional[List[str]] = None  # rutas locales de los archivos
    imagenes_embed: Optional[List[str]] = None  # rutas locales de imagenes embebidas