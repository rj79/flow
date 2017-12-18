from tests.test_common import FlowBaseTestCase as tc
from app import db
from app.model import User


class TestAuth(tc):
    def test_fail_login_if_unknown_user(self):
        response = self.client.post('/login',
                                    data={'email': 'jane@smith.com', 'password': 'secret'},
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://localhost/login', response.headers['Location'])
        response = self.client.get('/login',
                                    data={'email': 'jane@smith.com', 'password': 'secret'},
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertTrue(b'Invalid username or password' in response.data)

    def test_register_user_redirects_to_login_if_successful(self):
        response = self.client.post('/register',
                                    data={'name': 'Jane Smith', 'email': 'jane@smith.com',
                                    'password': 'secret', 'password2': 'secret'},
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://localhost/login', response.headers['Location'])

    def test_login_succeeds_if_user_exists(self):
        u = User(name='Jane Smith', email='jane@smith.com')
        u.set_password('secret')
        db.session.add(u)
        db.session.commit()
        response = self.client.post('/login',
                                    data={'email': 'jane@smith.com', 'password': 'secret'},
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://localhost/', response.headers['Location'])
