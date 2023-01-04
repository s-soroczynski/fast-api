from pydantic import BaseModel
from typing import List

from app.public_toilets import schemas


class User(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UserDetails(BaseModel):
    email: str
    public_toilets: List[schemas.PublicToilet]
