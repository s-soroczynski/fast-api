from sqlalchemy.orm import Session

from app.public_toilets import models, schemas
from app.users.schemas import User


def get_public_toilet(db: Session, id: int):
    return db.query(models.PublicToilet).filter(models.PublicToilet.id == id).first()


def get_public_toilet_by_name(db: Session, name: str):
    return (
        db.query(models.PublicToilet).filter(models.PublicToilet.name == name).first()
    )


def get_public_toilets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PublicToilet).offset(skip).limit(limit).all()


def get_user_public_toilets(db: Session, user_id: int):
    return (
        db.query(models.PublicToilet)
        .filter(models.PublicToilet.user_id == user_id)
        .all()
    )


def create_public_toilet(db: Session, item: schemas.PublicToilet, user: User):
    public_toilet = models.PublicToilet(
        name=item.name,
        lat=item.lat,
        lng=item.lng,
        user=user,
        description=item.description,
    )
    db.add(public_toilet)
    db.commit()
    db.refresh(public_toilet)
    return public_toilet
