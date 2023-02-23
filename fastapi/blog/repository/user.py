from sqlalchemy.orm import Session
from main import models, schemas
from main.hashing import Hash
from fastapi import HTTPException, status


def create(db:Session, request: schemas.User):
    new_usr = models.User(name = request.name, password = Hash.bcrypt(request.password), email = request.email)
    db.add(new_usr)
    db.commit()
    db.refresh(new_usr)
    return new_usr

def view(db:Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with id {id} not found !")
    return user