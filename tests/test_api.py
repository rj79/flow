import json
from tests.test_common import FlowBaseTestCase as tc
from app import create_app, db

class TestIssueTypeApi(tc):
    def test_can_return_all_issue_types(self):
        response = self.client.get('/api/issue_types')
        self.assertEqual(json.loads(response.get_data().decode('utf-8')),
            [{'id': 1, 'name': 'Story'},
             {'id': 2, 'name': 'Bug'}])
