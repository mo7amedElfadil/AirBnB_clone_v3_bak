#!/usr/bin/python3
""" holds class User"""
from hashlib import md5
from models.base_model import BaseModel, Base, db
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'
    if db:
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade='all, delete-orphan')
        reviews = relationship("Review", backref="user",
                               cascade='all, delete-orphan')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            pwd = md5()
            pwd.update(kwargs['password'].encode())
            self.password = pwd.hexdigest()
