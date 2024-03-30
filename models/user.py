#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        __password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="all, delete")
        reviews = relationship("Review", backref="user", cascade="all, delete")
    else:
        email = ""
        __password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """function to get User password"""
        return self.__password

    @password.setter
    def password(self, value):
        """function to set password"""
        if value:
            h = hashlib.new("md5")
            h.update(value.encode())
            self.__password = h.digest()
        else:
            raise TypeError("Password cannot be empty")
