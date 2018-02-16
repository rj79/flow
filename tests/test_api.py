import json
from tests.test_common import BaseTestCase as tc, get_json
from app import create_app, db

class TestIssueTypeApi(tc):
    def test_can_return_all_issue_types(self):
        self.login_user()
        response = self.client.get('/api/issue_types')
        self.assertEqual(get_json(response),
            [{'id': 1, 'name': 'Story'},
             {'id': 2, 'name': 'Bug'}])


class TestIssueListApi(tc):
    def test_create_issue(self):
        self.login_user()
        response = self.client.post('/api/issues',
                                    data={'issue_type': 2, 'title': 'Issue', 'description': 'Description'})
        self.assertEqual(201, response.status_code)
        d = get_json(response)
        self.assertEqual(1, d['id'])
        self.assertEqual(2, d['issue_type'])
        self.assertEqual('Issue', d['title'])
        self.assertEqual('Description', d['description'])

class TestProjectListApi(tc):
    def test_create_project(self):
        self.login_user()
        rv = self.client.post('/api/projects',
                              data={'key': 'proj', 'name': 'The Project'})

        self.assertEqual(201, rv.status_code)
        d = get_json(rv)
        self.assertEqual('PROJ', d['key'])
        self.assertEqual('The Project', d['name'])

    def test_create_project_fails_if_key_or_name_missing(self):
        self.login_user()
        rv = self.client.post('/api/projects',
                              data={'key': 'proj'})

        self.assertEqual(400, rv.status_code)

        rv = self.client.post('/api/projects',
                              data={'name': 'The Project'})

        self.assertEqual(400, rv.status_code)

    def test_create_project_fails_if_key_invalid(self):
        self.login_user()
        rv = self.client.post('/api/projects',
                              data={'key': '', 'name': 'The Project'})

        self.assertEqual(400, rv.status_code)

        rv = self.client.post('/api/projects',
                              data={'key': 'KE', 'name': 'The Project'})

        self.assertEqual(400, rv.status_code)

        rv = self.client.post('/api/projects',
                              data={'key': 'BEEFBEEFBEEFBEEFX', 'name': 'The Project'})

        self.assertEqual(400, rv.status_code)

        rv = self.client.post('/api/projects',
                              data={'key': 'A123', 'name': 'The Project'})
        self.assertEqual(400, rv.status_code)


class TestReleaseListApi(tc):
    def test_create_release(self):
        self.login_user()

        rv = self.client.post('/api/releases',
                              data={'name': 'R1', 'project_id': self.proj.id,
                                    'release_date': '20180216'})
        self.assertEqual(201, rv.status_code)

    def test_release_not_created_if_date_invalid(self):
        self.login_user()

        rv = self.client.post('/api/releases',
                              data={'name': 'R1', 'project_id': self.proj.id,
                                    'release_date': '201802160'})
        self.assertEqual(400, rv.status_code)

    def test_release_not_created_if_project_invalid(self):
        self.login_user()

        rv = self.client.post('/api/releases',
                              data={'name': 'R1', 'project_id': 999,
                                    'release_date': '20180216'})
        self.assertEqual(400, rv.status_code)
