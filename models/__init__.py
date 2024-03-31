#!/usr/bin/python3
"""Module creates a unique FileStorage instance for the application

Attrs:
    storage: an instance of FileStorage
"""

from os import getenv


db = (False, True)["db" == getenv("HBNB_TYPE_STORAGE")]

if db:
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
