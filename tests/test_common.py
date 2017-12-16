import unittest
from flask import current_app
from app import create_app, db
from model import Issue, Project, Release, Team, User

class FlowBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('unittest')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.proj = Project('TEST')
        db.session.add(self.proj)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()