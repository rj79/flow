from tests.test_common import FlowBaseTestCase as tc
from app import db
from app.common import IssueType
from app.model import Project, Issue


class TestIssue(tc):
    def test_can_create_and_query_issues(self):
        i1 = Issue(self.proj, IssueType.STORY, 'Issue 1')
        i2 = self.proj.create_issue(IssueType.DEFECT, 'Issue 2')

        db.session.add(i1)
        db.session.add(i2)
        db.session.commit()

        j1 = Issue.query.filter_by(id=1).first()
        j2 = Issue.query.filter_by(id=2).first()

        self.assertEqual('Issue 1', j1.title)
        self.assertEqual('Issue 2', j2.title)
        self.assertEqual(IssueType.STORY, j1.issue_type)
        self.assertEqual(IssueType.DEFECT, j2.issue_type)


class TestRelease(tc):
    def test_can_create_release(self):
        r = self.proj.create_release('First release')
        db.session.add(r)
        db.session.commit()
