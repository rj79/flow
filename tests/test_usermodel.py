import unittest
from app.model import User
from tests.test_common import BaseTestCase as tc

class UserModelTests(tc):
    def test_password_setter(self):
        u = User(name='Joe', email='user@domain')
        u.set_password('cat')
        self.assertTrue(u.pwhash is not None )

    def test_password_verification(self):
        u = User(name='Joe', email='user@domain')
        u.set_password('cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_password_salts_are_random(self):
        u1 = User(name='Joe', email='joe@domain')
        u2 = User(name='Sam', email='sam@domain')

        u1.set_password('cat')
        u2.set_password('cat')

        self.assertTrue(u1.pwhash != u2.pwhash)
