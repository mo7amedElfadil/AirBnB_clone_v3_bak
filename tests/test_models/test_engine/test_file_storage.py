#!/usr/bin/python3
"""
Unittest for the FileStorage Class
"""

import unittest
import datetime
import os
import models
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import inspect
import pycodestyle as pep8
from models.engine import file_storage
from models import db


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for FileStorage class
    documentation and pep8 conformaty"""

    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_file_storage conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_models/test_engine/' +
                                    'test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation"""
        mod_doc = file_storage.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self):
        """test class documentation"""
        mod_doc = str(FileStorage.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(FileStorage, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(FileStorage, inspect.ismethod))
        for func in base_funcs:
            self.assertTrue(len(str(func[1].__doc__)) > 0)


@unittest.skipIf(db, "not db")
class Test_attributes(unittest.TestCase):
    """This class defines unittests for the attributes of FileStorage class"""

    def test_type_path(self):
        """This function tests the type of __file_path attribute"""
        pack = FileStorage()
        self.assertIs(type(pack._FileStorage__file_path), str)

    def test_path_value(self):
        """This function tests the value of __file_path attr"""
        self.assertEqual("file.json", models.storage._FileStorage__file_path)

    def test_type_objs(self):
        """This function tests the type of the attribute __objects"""
        pack = FileStorage()
        self.assertIs(type(pack._FileStorage__objects), dict)

    def test_type_storage(self):
        """This function tests the type of the instant storage"""
        self.assertIs(type(models.storage), FileStorage)


@unittest.skipIf(db, "not db")
class Test_creating_objs(unittest.TestCase):
    """This class creates objects and checks storage instance changes"""

    @classmethod
    def setUpClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage.__objects = {}
        models.storage.all().clear()

    def tearDown(self):
        """removes files created and resets the value of __objects"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage.all().clear()

    def test_obj(self):
        """This function tests the contents of __objects and
        __file_path"""
        tdy = datetime.datetime.today()
        base = BaseModel(id="123456", created_at=tdy.isoformat(),
                         updated_at=tdy.isoformat())
        models.storage.new(base)
        base.save()
        self.assertTrue(os.path.exists("file.json"))
        objs = models.storage.all()
        self.assertIn("BaseModel.123456", objs)
        self.assertIs(type(objs["BaseModel.123456"]), BaseModel)

    def test_type_all(self):
        """This function tests the type of the return value method all of
        FileStorage"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_args(self):
        """This function tests the all method with an argument"""
        self.assertIs(type(models.storage.all(State)), dict)

    def test_all_dict(self):
        """This function tests all method dictionary"""
        base1 = BaseModel()
        base1.save()
        base2 = BaseModel()
        base2.save()
        base3 = BaseModel()
        base3.save()
        objs = models.storage.all()
        self.assertEqual(len(objs), 3)

    def test_new(self):
        """This function tests the mthod new of FileStorage"""
        base = BaseModel()
        usr = User()
        state = State()
        city = City()
        amenity = Amenity()
        place = Place()
        review = Review()
        models.storage.new(base)
        models.storage.new(usr)
        models.storage.new(state)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(place)
        models.storage.new(review)
        self.assertIn("BaseModel." + base.id, models.storage.all().keys())
        self.assertIn("User." + usr.id, models.storage.all().keys())
        self.assertIn("State." + state.id, models.storage.all().keys())
        self.assertIn("City." + city.id, models.storage.all().keys())
        self.assertIn("Amenity." + amenity.id, models.storage.all().keys())
        self.assertIn("Place." + place.id, models.storage.all().keys())
        self.assertIn("Review." + review.id, models.storage.all().keys())

    def test_new_args(self):
        """This function tests the new method with an argument"""
        with self.assertRaises(TypeError):
            models.storage.new()

        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        """This function tests for the save method of FileStorage"""
        base = BaseModel()
        base.save()
        usr = User()
        usr.save()
        state = State()
        state.save()
        city = City()
        city.save()
        amenity = Amenity()
        amenity.save()
        place = Place()
        place.save()
        review = Review()
        review.save()
        # All objs will be added automatically to __objects dict
        models.storage.save()
        with open("file.json", encoding="utf-8") as f:
            read_data = f.read()
            self.assertIn("BaseModel." + base.id, read_data)
            self.assertIn("User." + usr.id, read_data)
            self.assertIn("State." + state.id, read_data)
            self.assertIn("City." + city.id, read_data)
            self.assertIn("Amenity." + amenity.id, read_data)
            self.assertIn("Place." + place.id, read_data)
            self.assertIn("Review." + review.id, read_data)

    def test_save_args(self):
        """This function tests the save method with arguments"""
        with self.assertRaises(TypeError):
            models.storage.save("args")

    def test_reload(self):
        """This function tests the reload function"""
        base = BaseModel()
        base.save()
        usr = User()
        usr.save()
        state = State()
        state.save()
        city = City()
        city.save()
        amenity = Amenity()
        amenity.save()
        place = Place()
        place.save()
        review = Review()
        review.save()
        models.storage.save()
        models.storage._FileStorage__objects = {}
        models.storage.reload()
        objs = models.storage.all()
        self.assertIn("BaseModel." + base.id, objs)
        self.assertIn("User." + usr.id, objs)
        self.assertIn("State." + state.id, objs)
        self.assertIn("City." + city.id, objs)
        self.assertIn("Amenity." + amenity.id, objs)
        self.assertIn("Place." + place.id, objs)
        self.assertIn("Review." + review.id, objs)

    def test_reloading_without_save(self):
        """This function calls reload() without save()"""
        models.storage.reload()
        objs = models.storage.all()
        self.assertDictEqual({}, objs)

    def test_reload_args(self):
        """This function tests the method reload with no arguments"""
        with self.assertRaises(TypeError):
            models.storage.reload("args")

    def test_get(self):
        """This function tests the get method"""
        base = BaseModel()
        base.save()
        obj = models.storage.get(BaseModel, base.id)
        self.assertEqual(obj, base)

    def test_count(self):
        """This function tests the count method"""
        base = BaseModel()
        base.save()
        count = models.storage.count()
        self.assertEqual(count, 1)
        base2 = BaseModel()
        base2.save()
        count = models.storage.count()
        self.assertEqual(count, 2)
        count = models.storage.count(BaseModel)
        self.assertEqual(count, 2)
        count = models.storage.count(User)
        self.assertEqual(count, 0)


if __name__ == '__main__':
    unittest.main()
