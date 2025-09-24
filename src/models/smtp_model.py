from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict 

class EmailRequest(BaseModel):
    subject: str = Field(..., description="Asunto del correo")
    body: str = Field(..., description="Cuerpo del correo en formato HTML")
    to: EmailStr = Field(..., description="Destinatario principal del correo")
    identifying_name: str = Field(..., description="Identificador de plantillas")
    cc: Optional[List[EmailStr]] = Field(
        default=None, description="Lista de destinatarios en copia"
    )
    bcc: Optional[List[EmailStr]] = Field(
        default=None, description="Lista de destinatarios en copia oculta"
    )
    adjuntos: Optional[List[str]] = Field(
        default=None,
        description="Lista de rutas absolutas o relativas de archivos adjuntos",
        example=["/path/to/file.pdf", "docs/manual.docx"],
    )
    imagenes_embed: Optional[Dict[str, str]] = Field(
        default=None,
        description="Diccionario con imágenes a embeber en el cuerpo del correo. "
                    "Clave = Content-ID (cid), Valor = ruta al archivo de imagen.",
        example={"logo123": "static/images/logo.png"},
    )

    
    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Testing Email",
                "body": "<h1 style='font-size: 40px; color: crimson; text-align: center;'>❤️¡Hola!❤️</h1><p>Este es un correo de prueba con imagen embedida: <img src='cid:logo123'></p>",
                "to": "user@example.com",
                "identifying_name": "template1",
                "cc": ["user@example.com"],
                "bcc": ["user@example.com"],
                "adjuntos": ["/path/to/file.pdf", "docs/manual.docx"],
                "imagenes_embed": {"logo123": "static/images/logo.png"}
            }
        }

