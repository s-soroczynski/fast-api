from pydantic import BaseModel
from typing import Union


class PublicToilet(BaseModel):
    name: Union[str, None] = None
    lat: Union[float, None] = None
    lng: Union[float, None] = None
    description: Union[str, None] = None
    rate: Union[int, None] = 1

    class Config:
        orm_mode = True
