from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.template_model import Plantillas
from src.models.crud_model import CreateNotification,UpdateNotification


def consult_notifications(db: Session,skip: int = 0, limit: int = 10):
    return db.query(Plantillas).offset(skip).limit(limit).all()

def create_notification(db: Session, notification: CreateNotification):
    try:
        db_notification = Plantillas(**notification.dict())
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification
    except Exception as e: 
        raise HTTPException(
            status_code=500,
            detail="Error interno al crear la notificación"
        )

def read_notification(id_notification: int, db: Session):
    try:
        notification = db.query(Plantillas).filter(Plantillas.id == id_notification).first()
        if notification is None:
            raise HTTPException(status_code=404,detail=f"No se encontro notificacion con el ID: {id}, por favor verifique la informacion")
        return notification
    except Exception as e: 
        raise HTTPException(
            status_code=500,
            detail="Error interno al consultar la notificación"
        )

def update_notification(id_notification: int, data: UpdateNotification , db: Session):
    try:
        notification = db.query(Plantillas).filter(Plantillas.id == id_notification).first()
        if notification is None:
            raise HTTPException(status_code=404,detail=f"No se encontro notificacion con el ID: {id}, por favor verifique la informacion")
        data_dict = data.dict(exclude_unset=True)
        for campo, valor in data_dict.items():
            setattr(notification,campo,valor)
        db.commit()
        db.refresh(notification)
        return notification

    except Exception as e: 
        raise HTTPException(
            status_code=500,
            detail="Error interno al editar la notificación"
        )

def delete_notification(id_notification: int, db: Session):
    try:
        notification = db.query(Plantillas).filter(Plantillas.id == id_notification).first()
        if notification is None:
            raise HTTPException(status_code=404,detail=f"No se encontro notificacion con el ID: {id}, por favor verifique la informacion")
        db.delete(notification)
        db.commit()
        return {
            "message": "Notificacion eliminada correctamente",
            "status": "success",
            "data deleted": {notification}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al eliminar el producto", error = e)

