#!/usr/bin/python3
"""
Unittest for the Class "City"
"""

import io
import unittest
import datetime
import uuid
import models
from unittest.mock import patch
from models.city import City
import inspect
import pycodestyle as pep8
import models.city as city_model
from models import db


class TestCityDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""

    def test_pep8_city(self) -> None:
        """Test that the city_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_city(self) -> None:
        """Test that the test_city_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_models/test_city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = city_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(City.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        city_funcs = inspect.getmembers(City, inspect.isfunction)
        city_funcs.extend(inspect.getmembers(City, inspect.ismethod))
        for func in city_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


@unittest.skipIf(db, "not db")
class Test_City(unittest.TestCase):
    '''Test City class'''

    def test_docstr(self):
        '''Test class documentaion'''
        self.assertTrue(len(City.__doc__) > 2)

    def test_init(self):
        '''Test instances/cls attrs exists'''
        rev = City()
        # instance attrs
        self.assertTrue(hasattr(rev, 'id'))
        self.assertTrue(hasattr(rev, 'created_at'))
        self.assertTrue(hasattr(rev, 'updated_at'))
        # cls attrs
        self.assertTrue(hasattr(rev, 'name'))
        self.assertTrue(hasattr(rev, 'state_id'))

    def test_type_attrs(self):
        '''Test instance types'''
        rev = City()
        # instance attrs
        self.assertIsInstance(rev.id, str)
        self.assertIsInstance(rev.created_at, datetime.datetime)
        self.assertIsInstance(rev.updated_at, datetime.datetime)
        # cls attrs
        self.assertIsInstance(rev.name, str)
        self.assertIsInstance(rev.state_id, str)

    def test_args(self):
        '''Test anonymous arguments'''
        id = str(uuid.uuid4())
        rev = City(id)
        self.assertNotEqual(id, rev.id)

    def test_kwargs(self):
        '''Test named arguments'''
        kw = {
            'id': 1, 'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        with self.assertRaises(TypeError):
            City(**kw)
        kw['created_at'] = datetime.datetime.now().isoformat()
        kw['updated_at'] = datetime.datetime.now().isoformat()
        rev = City(**kw)
        self.assertEqual(rev.id, kw['id'])
        self.assertEqual(rev.created_at.isoformat(), kw['created_at'])
        self.assertEqual(rev.updated_at.isoformat(), kw['updated_at'])

    def test_save(self):
        '''Test saving object to file.json'''
        rev = City()
        prev_date = rev.updated_at
        rev.save()
        curr_date = rev.updated_at

        self.assertIn('City'+'.'+rev.id,
                      models.storage.all(City).keys())
        self.assertNotEqual(prev_date.isoformat(), curr_date.isoformat())
        with self.assertRaises(TypeError):
            rev.save('')

    def test_to_dict(self):
        '''Test `to_dict` method'''
        rev = City()
        dct = rev.to_dict()
        self.assertIn('__class__', dct)
        self.assertEqual('City', dct['__class__'])
        with self.assertRaises(TypeError):
            rev.to_dict({'id': '123'})
            City()

    def test_str(self):
        '''Test `City` representaion'''
        with patch('sys.stdout', new_callable=io.StringIO) as m_stdout:
            rev = City()
            print(rev)
            self.assertEqual(m_stdout.getvalue(),
                             '[City] ({}) {}\n'.format(rev.id, rev.__dict__))


if __name__ == '__main__':
    unittest.main()
