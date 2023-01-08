from pydantic import BaseModel


class PublicToilet(BaseModel):
    name: str
    lat: float
    lng: float
    description: str

    class Config:
        orm_mode = True
