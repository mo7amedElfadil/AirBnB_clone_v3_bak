#!/usr/bin/python3
""" holds class State"""
from models.base_model import BaseModel, Base, db
from models.city import City
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of state """
    __tablename__ = 'states'
    if db:
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade='all, delete-orphan')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if not db:
        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            from models import storage
            city_list = []
            all_cities = storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
