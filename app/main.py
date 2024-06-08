from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, schemas
from datetime import datetime 
from typing import List

app = FastAPI()

# Recreate the database tables, load fixtures on restart
models.Base.metadata.drop_all(bind=database.engine)
models.Base.metadata.create_all(bind=database.engine)


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

coffees = [
    {
        "id": 1,
        "name": "Kenia Gachami AA Washed",
        "manufacturer": "Heresy",
        "rating": 5.0,
        "country": "Kenia",
        "cupping_score": "87.5 / 100 pkt",
        "processing": "washed",
        "roast": "jasno palona",
        "notes": "owocowa, soczysta, pełna słodyczy",
        "image_url": "TODO"
    }
]

reviews = [
    {
        "id": 1,
        "coffee_id": 1,
        "rating": 4.0,
        "review": "Prawdziwa perełka. Jej stopień palenia idealnie nadaje się do przelewowych metod parzenia, a bogaty profil smakowy wypełniony owocowością i słodyczą zachwyca z każdym łykiem.\n\nTo kawa, która zachwyci nawet najbardziej wymagających koneserów. \n\nOpakowanie w postaci brązowego słoika PET jest bardzo eco-friendly! ♻️\n\nOdejmuję jedną gwiazdkę za to, że wstałem lewą nogą z łóżka.",
        "date": datetime.now(),
        "user": "Maciej Kaszkowiak",
        "image_url": "TODO"
    }
]

with database.SessionLocal() as db:
    for data in coffees:
        model = models.Coffee(**data)
        db.add(model)
    
    for data in reviews:
        model = models.Review(**data)
        print("adding", model)
        db.add(model)
    db.commit()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/coffee", response_model=list[schemas.Coffee])
def get_coffee(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    response = db.query(models.Coffee).offset(skip).limit(limit).all()
    return response