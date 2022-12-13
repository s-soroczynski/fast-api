from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.utils import get_db
from app.public_toilets import crud, schemas
from app.users.models import User
from app.users.utils import get_current_user


router = APIRouter(
    prefix="/public-toilets",
    tags=["public-toilets"],
)


@router.get("/")
async def public_toilets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_public_toilets = crud.get_public_toilets(db, skip=skip, limit=limit)
    return db_public_toilets


@router.post("/")
async def public_toilets(public_toilet: schemas.PublicToilet, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_public_toilet = crud.get_public_toilet_by_name(db, name=public_toilet.name)
    if db_public_toilet:
        raise HTTPException(status_code=400, detail="Name already taken")
    return crud.create_public_toilet(db=db, public_toilet=public_toilet, user=current_user)