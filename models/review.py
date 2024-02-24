#!/usr/bin/python3
""" Review module for the HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """ Review class to store review information """
    __tablename__ = "reviews"
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    text = Column(Text(1024), nullable=False)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        users = relationship('User', back_populates="reviews",
                             cascade="all, delete")
        place = relationship('Place', back_populates="reviews",
                             cascade="all, delete")

    else:
        place_id = ""
        user_id = ""
        text = ""
