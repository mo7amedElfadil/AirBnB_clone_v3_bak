#!/usr/bin/python3
"""Module defines Amenity"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
import models

class Amenity(BaseModel, Base):
    """Representation of Amenity """
    __tablename__ = 'amenities'
    if models.db:
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
