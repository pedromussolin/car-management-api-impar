from fastapi import FastAPI, HTTPException, Depends, Query, Response
from pydantic import BaseModel
from typing import Annotated, Optional
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from base64 import b64decode
from io import BytesIO
from PIL import Image
import models


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class CarBase(BaseModel):
    Name: str
    Status: int
    Photo_id: int

class PhotoBase(BaseModel):
    Base64: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/cars/{car_name}")  # Mark car_name endpoint as deprecated
async def read_car(car_name: str, db: db_dependency, skip: int = 0, limit: int = 10): # type: ignore
    result = db.query(models.Car).filter(models.Car.Name == car_name).offset(skip).limit(limit).first()
    if not result:
        raise HTTPException(status_code=404, detail='Carro não encontrado')
    return {"Id": result.id, "Name": result.Name, "Status": result.Status, "PhotoId": result.Photo_id}


@app.post("/cars/")
async def create_car(car: CarBase, db: db_dependency): # type: ignore
    db_car = models.Car(Name=car.Name, Status=car.Status, Photo_id=car.Photo_id)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)


@app.put("/cars/{car_id}")
async def update_car(car_id: int, car: CarBase, db: db_dependency): # type: ignore
    try:
        db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
        if not db_car:
            raise HTTPException(status_code=404, detail="Carro não encontrado")

        db_car.Name = car.Name
        db_car.Status = car.Status
        db_car.Photo_id = car.Photo_id

        db.commit()
        db.refresh(db_car)
        return db_car
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar carro: {str(e)}")


@app.delete("/cars/{car_id}")
async def delete_car(car_id: int, db: db_dependency): # type: ignore
    try:
        db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
        if not db_car:
            raise HTTPException(status_code=404, detail="Carro não encontrado")

        db.delete(db_car)
        db.commit()
        return {"detail": "Carro excluído com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir carro: {str(e)}")


@app.get("/cars")
async def get_cars(db: db_dependency, skip: int = 0, limit: int = 10): # type: ignore
    cars = db.query(models.Car).offset(skip).limit(limit).all()
    return [{"Id": car.id, "Name": car.Name, "Status": car.Status, "PhotoId": car.Photo_id} for car in cars]


@app.get("/cars/{car_id}/photo")
async def get_car_photo(car_id: int, db: db_dependency): # type: ignore
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Carro não encontrado")

    if not car.Photo_id:
        raise HTTPException(status_code=404, detail="Carro não possui foto")

    photo = db.query(models.Photo).filter(models.Photo.id == car.Photo_id).first()
    if not photo:
        raise HTTPException(status_code=500, detail="Foto não encontrada no banco de dados")

    try:
        image_data = b64decode(photo.Base64)
        image = Image.open(BytesIO(image_data))
        content_type = "image/" + image.format.lower()
    except IOError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao abrir a imagem: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a imagem: {str(e)}")

    return Response(content=image_data, media_type=content_type)