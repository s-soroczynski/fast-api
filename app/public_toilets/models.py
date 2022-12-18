from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database import Base


class PublicToilet(Base):
    __tablename__ = "public_toilet"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lng = Column(Float, index=True)
    lat = Column(Float, index=True)
    rate = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="public_toilet")
