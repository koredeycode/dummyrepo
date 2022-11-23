#!/usr/bin/python3
"""Contains class FileStorage"""

import json
from models.base_model import BaseModel
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User


class FileStorage():
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return (FileStorage.__objects)

    def new(self, obj):
        """sets in __objests the obj with key <obj class name>.id"""
        ocn = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocn, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        objs_dict = FileStorage.__objects
        obj_dicts = {}
        for obj_key in objs_dict.keys():
            obj_dicts[obj_key] = objs_dict[obj_key].to_dict()
        """obj_dicts = {obj_key: objs_dict[obj_key].to_dict()
        for obj_key in objs_dict.keys()}"""

        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dicts, f)

    def reload(self):
        """deserializes the JSON file to __objects only if the
        __filepath exists"""
        try:
            with open(FileStorage.__file_path) as f:
                obj_dicts = json.load(f)
                for obj in obj_dicts.values():
                    cls_name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(cls_name)(**obj))
        except FileNotFoundError:
            return
