from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from datetime import datetime
from app import db

class Project(db.Model):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    key = Column(String(16))
    name = Column(String(256))

    def create_issue(self, title):
        issue = Issue(self)
        return issue

class Release(db.Model):
    __tablename__ = 'releases'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    date = Column(DateTime)


class Team(db.Model):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))


class Issue(db.Model):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    created_date = Column(db.DateTime, nullable=False, default=datetime.utcnow())
    title = Column(String(256))
    description = Column(String(1024))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    target_release_id = db.Column(db.Integer, ForeignKey('releases.id'), nullable=True)
    team_id = db.Column(db.Integer, ForeignKey('teams.id'), nullable = True)

    project = db.relationship('Project')
    target_release = db.relationship('Release')
    team = db.relationship('Team')

    def __init__(self, project):
        self.project = project
        self.description = None

    def __repr__(self):
        return '<Issue "%s">' % (self.title)
