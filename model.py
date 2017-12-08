from sqlalchemy import Column, DateTime, Integer, String
from database import Base


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    key = Column(String(16))
    name = Column(String(256))


class Release(Base):
    __tablename__ = 'releases'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    date = Column(DateTime)


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))


class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    title = Column(String(256))
    description = Column(String(1024))
    project = db.relationship('Project')
    target_release = db.relationship('Release')
    team = db.relationship('Team')

    def __init__(self, title):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<Issue %s>' % (self.name)
