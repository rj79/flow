from tests.test_common import FlowBaseTestCase as tc
from app import db

class TestIssue(tc):
    def test_can_create_issue(self):
        i = self.proj.create_issue('Issue')
        db.session.add(i)
        db.session.commit()


class TestRelease(tc):
    def test_can_create_release(self):
        r = self.proj.create_release('First release')
        db.session.add(r)
        db.session.commit()
