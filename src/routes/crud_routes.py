from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.config import get_session
from src.models.crud_model import Notification, CreateNotification
from src.services.crud_services import create_notification,consult_notifications


# inicializacion del roter 
crud_routes = APIRouter()



@crud_routes.get("/notifications/", response_model=list[Notification])
def  list_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    return consult_notifications(db,skip=skip,limit=limit)

@crud_routes.post("/notifications/", response_model=Notification)
def create_product(notification: CreateNotification, db: Session = Depends(get_session)):
    return create_notification(db, notification)