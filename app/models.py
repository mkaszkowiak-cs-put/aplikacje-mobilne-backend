from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Coffee(Base):
    __tablename__ = "coffees"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    manufacturer = Column(String, index=True)
    rating = Column(Float)
    image_url = Column(String)
    country = Column(String, index=True)
    cupping_score = Column(String, index=True)
    processing = Column(String, index=True)
    roast = Column(String, index=True)
    notes = Column(String, index=True)
    reviews = relationship("Review", back_populates="coffee")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float)
    user = Column(String)
    review = Column(String)
    image_url = Column(String)
    date = Column(DateTime)
    coffee_id = Column(Integer, ForeignKey("coffees.id"))
    coffee = relationship("Coffee", back_populates="reviews")