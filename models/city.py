#!/usr/bin/python3
"""Module defines City"""

from models.base_model import BaseModel, Base, store
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models


class City(BaseModel, Base):
    """Representation of city """
    __tablename__ = 'cities'
    if models.db:
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade='all, delete-orphan')
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
