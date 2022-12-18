from pydantic import BaseModel


class PublicToilet(BaseModel):
    name: str
    lat: float
    lng: float
    rate: int

    class Config:
        orm_mode = True
