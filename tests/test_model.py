import unittest
from flask import current_app
from app import create_app, db
from model import Issue, Project, Release, Team, User

class CommonTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app('unittest')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.proj = Project()
        db.session.add(self.proj)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestIssue(CommonTestClass):
    def test_can_create_issue(self):
        i = self.proj.create_issue()
        db.session.add(i)
        db.session.commit()


class TestRelease(CommonTestClass):
    def test_can_create_release(self):
        r = self.proj.create_release('First release')
        db.session.add(r)
        db.session.commit()
