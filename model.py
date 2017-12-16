from app import db
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from werkzeug import generate_password_hash, check_password_hash
from common import State

class Project(db.Model):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    key = Column(String(16), nullable=False, unique=True)
    name = Column(String(256))

    def __init__(self, key):
        self.key = key

    def create_issue(self, issue_type, title):
        issue = Issue(self, issue_type, title)
        return issue

    def create_release(self, name):
        release = Release(self)
        release.name = name
        return release

    def __repr__(self):
        return "<Project id=%d key='%s'>" % (self.id, self.key)


class Release(db.Model):
    __tablename__ = 'releases'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    date = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project')

    def __init__(self, project):
        self.project = project


class Team(db.Model):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))


class Issue(db.Model):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    issue_type = Column(Integer)
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    state = Column(Integer, default=State.CREATED)
    resolution = Column(Integer)
    title = Column(String(256), nullable=True)
    description = Column(String(1024))
    blocked = Column(Boolean, default=False)
    reopen_count = Column(Integer, default=0)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    target_release_id = Column(Integer, ForeignKey('releases.id'), nullable=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable = True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    assignee_id = Column(Integer, ForeignKey('users.id'))

    project = db.relationship('Project')
    target_release = db.relationship('Release')
    team = db.relationship('Team')
    creator = db.relationship('User', foreign_keys=[creator_id])
    assignee = db.relationship('User', foreign_keys=[assignee_id])

    def __init__(self, project, issue_type, title):
        self.project_id = project.id
        self.issue_type = issue_type
        self.title = title

    def reopen(self):
        self.state = common.OPEN
        self.reopen_count += 1

    def get_key(self):
        return "%s-%d" % (self.project.key, self.id)

    def __repr__(self):
        return '<Issue "%s">' % (self.title)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow())
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

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
