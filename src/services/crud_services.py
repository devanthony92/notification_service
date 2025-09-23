from sqlalchemy.orm import Session
from src.models.template_model import Plantillas
from src.models.crud_model import CreateNotification



def create_notification(db: Session, notification: CreateNotification):
    db_notification = Plantillas(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def consult_notifications(db: Session,skip: int = 0, limit: int = 10):
    return db.query(Plantillas).offset(skip).limit(limit).all()