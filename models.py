from sqlalchemy import Column, ForeignKey, Integer, String, Text
from database import Base


class Car(Base):
    __tablename__ = 'API_car'

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)
    Status = Column(Integer, index=True)
    Photo_id = Column(Integer, ForeignKey("API_photo.id"), index=True)


class Photo(Base):
    __tablename__ = 'API_photo'

    id = Column(Integer, primary_key=True, index=True)
    Base64 = Column(Text, index=True)