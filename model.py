from app import db
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from werkzeug import generate_password_hash, check_password_hash


class Project(db.Model):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    key = Column(String(16))
    name = Column(String(256))

    def create_issue(self, title=None):
        issue = Issue(self)
        if title is not None:
            issue.title = title
        return issue

    def create_release(self, name):
        release = Release(self)
        release.name = name
        return release

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
    type = Column(Integer)
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    title = Column(String(256))
    description = Column(String(1024))
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    target_release_id = Column(Integer, ForeignKey('releases.id'), nullable=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable = True)

    project = db.relationship('Project')
    target_release = db.relationship('Release')
    team = db.relationship('Team')

    def __init__(self, project):
        self.project = project
        self.description = None

    def __repr__(self):
        return '<Issue "%s">' % (self.title)


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
