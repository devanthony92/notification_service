
from datetime import datetime
from pydantic import BaseModel, constr
from typing import Optional


class Notification(BaseModel):
    id: int
    identifying_name: constr(min_length=1,max_length=100) 
    description: constr(min_length=2,max_length=255)
    content_html: constr(min_length=2,max_length=255)
    created_at: datetime | None = None

    class Config:
        from_attributes = True # Esto permite convertir desde SQLAlchemy a Pydantic

class CreateNotification(BaseModel):
    identifying_name: constr(min_length=1,max_length=100) 
    description: constr(min_length=2,max_length=255)
    content_html: constr(min_length=2,max_length=255)

class UpdateNotification(BaseModel):
    identifying_name: Optional[constr(min_length=1,max_length=100)] = None
    description: Optional[constr(min_length=1,max_length=255)] = None
    content_html:  Optional[constr(min_length=1,max_length=255)] = None

    class Config:
        from_attributes = True # Esto permite convertir desde SQLAlchemy a Pydantic
