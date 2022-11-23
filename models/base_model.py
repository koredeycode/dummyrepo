#!/usr/bin/python3
"""This contain the class BaseModel"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel():
    """Defines all common attributes/methods for other classes"""
    def __init__(self, *args, **kwargs):
        """the initialization function"""
        if kwargs and len(kwargs) > 0:
            for k, v in kwargs.items():
                if k == "__class__":
                    continue
                else:
                    if k == "created_at" or k == "updated_at":
                        self.__dict__[k] = datetime.fromisoformat(v)
                    else:
                        self.__dict__[k] = v
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return the string representation of a class"""
        cn = self.__class__.__name__
        return "[{}] ({}) {}".format(cn, self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute updated_at with the
        current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of ___dict
        of the instance"""
        sd = self.__dict__.copy()
        sd["__class__"] = self.__class__.__name__
        sd["created_at"] = self.created_at.isoformat()
        sd["updated_at"] = self.updated_at.isoformat()
        return (sd)
