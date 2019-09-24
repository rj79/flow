from app import login_manager
from app.common import State, issue_type_name
from database import db
from datetime import datetime, time, date
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from werkzeug import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except ValueError:
        return None

def today():
    return date.today()

def utcnow():
    return datetime.utcnow()

class Project(db.Model):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    key = Column(String(16), nullable=False, unique=True)
    name = Column(String(256))

    def __init__(self, key, name):
        self.key = key
        self.name = name

    def create_issue(self, issue_type, title):
        issue = Issue(self, issue_type, title)
        return issue

    def create_release(self, name, date):
        return Release(self, name, date)

    def __repr__(self):
        return "<Project id=%d key='%s'>" % (self.id, self.key)


class Release(db.Model):
    __tablename__ = 'releases'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    release_date = Column(Date)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project', backref='releases', lazy=True)

    def __init__(self, project, name, date):
        self.project = project
        self.name = name
        self.release_date = date


class Team(db.Model):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

class IssueType(db.Model):
    __tablename__ = 'issuetypes'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)

class Issue(db.Model):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, nullable=False, default=utcnow)
    state = Column(Integer, default=State.CREATED)
    resolution = Column(Integer)
    title = Column(String(256), nullable=True)
    description = Column(String(1024))
    blocked = Column(Boolean, default=False)
    reopen_count = Column(Integer, default=0)
    requirement_link = Column(String(256), nullable=True)
    issue_type_id = Column(Integer, ForeignKey('issuetypes.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    target_release_id = Column(Integer, ForeignKey('releases.id'), nullable=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable = True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    assignee_id = Column(Integer, ForeignKey('users.id'))

    project = db.relationship('Project')
    target_release = db.relationship('Release')
    team = db.relationship('Team')
    creator = db.relationship('User', foreign_keys=[creator_id])
    assignee = db.relationship('User', foreign_keys=[assignee_id])
    issuetype = db.relationship('IssueType')

    def __init__(self, project, issue_type, title):
        self.project_id = project.id
        self.issue_type_id = issue_type
        self.title = title

    def reopen(self):
        self.state = common.OPEN
        self.reopen_count += 1

    @property
    def key(self):
        return f'{self.project.key}-{self.id}'

    def typename(self):
        try:
            return issue_type_name[self.issue_type_id]
        except:
            return "Unknown type"

    def __repr__(self):
        return f'<Issue "{self.key}">'


"""
Association table for issue_dependencies between issues
TODO: Find better column names! :-)
"""
"""
dependency_table = Table('issue_dependencies', db.Model.metadata,
    Column('needing_id', Integer, ForeignKey('issues.id')),
    Column('fulfilling_id', Integer, ForeignKey('issues.id'))
)
"""


class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=utcnow)
    text = Column(String(1024))

    issue_id = Column(Integer, ForeignKey('issues.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    issue = db.relationship('Issue', backref=db.backref('comments'), lazy=True)
    user = db.relationship('User', backref=db.backref('comments'), lazy=True)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(128), unique=True)
    pwhash = Column(String(256))
    enabled = Column(Boolean, default=False)

    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(64), unique=True)
    email_verification_expiration = Column(DateTime)

    pw_reset_token = Column(String(64), unique=True)
    pw_reset_token_expiration = Column(DateTime)

    def set_password(self, password):
        self.pwhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    """ Used by flask-login"""
    def is_authenticated(self):
        return True

    """ Used by flask-login"""
    def is_active(self):
        return True

    """ Used by flask-login"""
    def is_anonymous(self):
        return False

    """ Used by flask-login"""
    def get_id(self):
        return str(self.id)

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)
