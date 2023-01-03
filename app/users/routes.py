from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session

from app.users import crud, schemas, models, utils
from app.utils import get_db
from app.public_toilets import crud as public_toilets_crud


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
async def users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = crud.get_users(db, skip=skip, limit=limit)
    return db_users


@router.get("/me")
async def get_user_me(current_user: models.User = Depends(utils.get_current_user)):
    # TODO should we return hashed password? Fix test if no, trelo #13
    return current_user


@router.get('/{id}', response_model=schemas.UserDetails)
async def get_user(id: int = Path(), db = Depends(get_db), current_user: models.User = Depends(utils.get_current_user)):
    if id != current_user.id:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user_public_toilets = public_toilets_crud.get_user_public_toilets(db, user_id=current_user.id)
    user_details: schemas.UserDetails = {"email": current_user.email, "public_toilets": db_user_public_toilets}
    return user_details


@router.post("/", status_code=201)
async def create_users(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exist")
    return crud.create_user(db=db, user=user)

