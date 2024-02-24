#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship
from models.place import Place
from models.review import Review


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    if getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship('Place', back_populates="user",
                              cascade="all, delete")
        reviews = relationship('Review', back_populates="users",
                               cascade="all, delete")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
