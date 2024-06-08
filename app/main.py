from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, schemas
from datetime import datetime 
from typing import List
from fastapi import HTTPException

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
    },
    {
        "id": 2,
        "name": "Very Berry Filter",
		"manufacturer": "COFFEE PLANT",
		"rating": 4.0,
        "country": "Rwanda / Etopia",
        "cupping_score": "84.5 / 87 pkt",
        "processing": "natural",
        "roast": "jasno palona",
        "notes": "wiśnie, porzeczki, śliwki",
		"image_url": "TODO",
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
    },
    {
        "id": 2,
        "coffee_id": 1,
        "rating": 1.0,
        "review": "Ta kawa z Kenii to kolejna przereklamowana propozycja, która nie zasługuje na tyle uwagi, ile się jej poświęca. \n\nPalona w jakiejś tam palarni przez Wicemistrza Polski Roasting 2020 – serio? Czy to jest powód, żeby uznać ją za coś wyjątkowego? \n\nJasna paloność? Owszem, jak dla mnie to po prostu niedopalone ziarna. A ta \"wysoka owocowość\"? To tylko chwyt marketingowy. Kawa ma być kawą, a nie jakimś soczystym owocem. Poza tym, co to za wynik w cuppingu - 87.5 na 100? To nie ocena, to jakaś loteria. I ten plastikowy słoik, który niby jest eco-friendly? Śmiech na sali. W czasach, gdy powinniśmy dbać o środowisko, proponują nam plastik. Lepiej zainwestować w porządną kawę, a nie w ten bubel.",
        "date": datetime.now(),
        "user": "Adam Jałocha",
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

@app.post("/review", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    coffee = db.query(models.Coffee).filter(models.Coffee.id == review.coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    new_review = models.Review(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review