from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, Unicode, UnicodeText, DateTime
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


meta_tag = Table(
    'meta_tag', Base.metadata,
    Column('meta_id', Integer, ForeignKey('meta.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

meta_person = Table(
    'meta_person', Base.metadata,
    Column('meta_id', Integer, ForeignKey('meta.id')),
    Column('person_id', Integer, ForeignKey('person.id'))
)

meta_branch = Table(
    'meta_branch', Base.metadata,
    Column('meta_id', Integer, ForeignKey('meta.id')),
    Column('branch_id', Integer, ForeignKey('branch.id'))
)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, ForeignKey('meta.id'), primary_key=True)
    title = Column('title', Unicode(300), nullable=False)
    description = Column('description', Unicode(2000))
    text = Column('text', UnicodeText(), nullable=False)

    meta = relationship("Meta", backref=backref("post", uselist=False))


class Meta(Base):
    __tablename__ = "meta"

    id = Column(Integer, primary_key=True)
    visit_ts = Column(DateTime(), nullable=False)
    link = Column('link', String(80), nullable=False, unique=True)
    parent_link = Column('parent_link', String(80), nullable=False)
    campus = Column('campus', Unicode(20), nullable=False)
    section = Column('section', Unicode(80), nullable=False)
    date = Column('date', Date())

    tags = relationship('Tag', secondary='meta_tag',
                        lazy='dynamic', backref="meta")

    branches = relationship('Branch', secondary='meta_branch',
                            lazy='dynamic', backref="meta")

    people = relationship('Person', secondary='meta_person',
                          lazy='dynamic', backref="meta")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column('name', Unicode(60), unique=True)


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column('name', Unicode(80), unique=True)


class Branch(Base):
    __tablename__ = "branch"

    id = Column(Integer, primary_key=True)
    name = Column('name', Unicode(80), unique=True)
