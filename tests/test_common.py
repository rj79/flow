from app import create_app
from app.model import Issue, Project, Release, Team, User, db
from flask import current_app, url_for
from tests.csrf_decorator import FlaskClient
import json
import unittest

def get_json(response):
    return json.loads(response.get_data().decode('utf-8'))

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('unittest')
        self.app.test_client_class = FlaskClient
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()
        db.create_all()

        self.proj = Project('TEST', 'Test project')
        db.session.add(self.proj)

        self.user = User(name='tester', email='testuser@local.net')
        self.user.set_password('password')
        db.session.add(self.user)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login_user(self):
        return self.login('testuser@local.net', 'password').data

    def login(self, email, password):
        return self.client.post('/login',
                                data={'email': email,
                                      'password': password,
                                      'csrf_token': self.client.csrf_token},
                                follow_redirects=True)
