from fastapi import APIRouter, HTTPException, Depends, Path
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
async def public_toilets(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    db_public_toilets = crud.get_public_toilets(db, skip=skip, limit=limit)
    return db_public_toilets


@router.get("/{id}")
async def public_toilets(id: int = Path, db: Session = Depends(get_db)):
    db_public_toilet = crud.get_public_toilet(db, id)
    if db_public_toilet is None:
        raise HTTPException(
            status_code=404,
            detail=f"Public toilet with id {id} does not exist",
        )
    return db_public_toilet


@router.post("/", status_code=201)
async def public_toilets(
    public_toilet: schemas.PublicToilet,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_public_toilet = crud.get_public_toilet_by_name(db, name=public_toilet.name)
    if db_public_toilet:
        raise HTTPException(status_code=400, detail="Name already taken")
    return crud.create_public_toilet(
        db=db, public_toilet=public_toilet, user=current_user
    )


@router.patch("/{id}", response_model=schemas.PublicToilet)
async def update_public_toilet(
    id: str,
    item: schemas.PublicToilet,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    existing_item = crud.get_public_toilet(db, id)
    if existing_item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Public toilet with id {id} does not exist",
        )
    return crud.update_public_toilet(db, item=item, id=id)