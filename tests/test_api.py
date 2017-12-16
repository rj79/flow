import json
from tests.test_common import FlowBaseTestCase as tc, get_json
from app import create_app, db


class TestIssueTypeApi(tc):
    def test_can_return_all_issue_types(self):
        response = self.client.get('/api/issue_types')
        self.assertEqual(get_json(response),
            [{'id': 1, 'name': 'Story'},
             {'id': 2, 'name': 'Bug'}])


class TestIssueListApi(tc):
    def test_create_issue(self):
        response = self.client.post('/api/issues',
                                    data={'issue_type': 2, 'title': 'Issue', 'description': 'Description'},
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(201, response.status_code)
        d = get_json(response)
        self.assertEqual(1, d['id'])
        self.assertEqual(2, d['issue_type'])
        self.assertEqual('Issue', d['title'])
        self.assertEqual('Description', d['description'])
