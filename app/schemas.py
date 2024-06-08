from typing import List, Optional
from pydantic import BaseModel
from pydantic.datetime_parse import parse_datetime
import datetime

class UTCDatetime(datetime.datetime):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime  # default Pydantic behavior
        yield cls.validate

    @classmethod
    def validate(cls, value) -> str:
        if value.tzinfo is None:
            return value.replace(tzinfo=datetime.timezone.utc)

        # Convert to UTC
        return value.astimezone(datetime.timezone.utc)
        # or alternatively, return the original value:
        # return value

class ReviewBase(BaseModel):
    rating: float
    user: str
    review: str
    date: UTCDatetime

    class Config:
        orm_mode = True

class ReviewCreate(ReviewBase):
    coffee_id: int
    class Config:
        orm_mode = True

class Review(ReviewBase):
    id: int
    coffee_id: int
    image_url: Optional[str] = None
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
