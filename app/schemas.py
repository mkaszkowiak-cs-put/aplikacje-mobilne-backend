from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ReviewBase(BaseModel):
    rating: float
    user: str
    review: str
    image_url: Optional[str] = None
    date: datetime

    class Config:
        orm_mode = True

class ReviewCreate(ReviewBase):
    coffee_id: int
    class Config:
        orm_mode = True

class Review(ReviewBase):
    id: int
    coffee_id: int
    class Config:
        orm_mode = True

class Coffee(BaseModel):
    id: int
    reviews: List[Review] = []
    name: str
    manufacturer: str
    rating: Optional[float] = None
    image_url: Optional[str] = None
    country: str
    cupping_score: str
    processing: str
    roast: str
    notes: str
    class Config:
        orm_mode = True
