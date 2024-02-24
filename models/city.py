#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        states = relationship('State', back_populates='cities',
                              cascade='all, delete')
        places = relationship('Place', back_populates='cities',
                              cascade='all, delete')
    else:
        name = ""
        state_id = ""
