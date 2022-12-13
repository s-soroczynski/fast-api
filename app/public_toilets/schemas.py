from pydantic import BaseModel


class PublicToilet(BaseModel):
    name: str
    lat: float
    lng: float

    class Config:
        orm_mode = True
