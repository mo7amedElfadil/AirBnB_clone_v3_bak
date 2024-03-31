#!/usr/bin/python3
"""Module defines BaseModel class"""

from uuid import uuid4
import models
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

if models.db:
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """BaseModel class"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    def __init__(self, *_, **kwargs):
        """Instantiate an instance"""
        self.id = str(uuid4())
        if not len(kwargs):
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            return
        for k, v in kwargs.items():
            if k != "__class__":
                setattr(self, k, v if k not in ("updated_at", "created_at")
                        else datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f"))

    def save(self):
        """updates the public instance attribute updated_at"""

        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__

        Return:
            dictionary representaion of class attributes,
                with `__class__` attr to manifest class instance
        """
        _dict = {k: v.isoformat() if isinstance(v, datetime) else
                 v for k, v in self.__dict__.items()
                 if k != "_sa_instance_state"}
        _dict["__class__"] = self.__class__.__name__
        return _dict

    def delete(self):
        """deletes the current instance from the storage"""
        models.storage.delete(self)

    def __str__(self):
        """Instance representaion"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
