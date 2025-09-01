from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class School(Base):
    __tablename__ = "schools"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Learner(Base):
    __tablename__ = "learners"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    school_id = Column(Integer, ForeignKey("schools.id"))

class Homework(Base):
    __tablename__ = "homework"
    id   = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    task = Column(Text)
    special_focus = Column(Text)
    learner_id = Column(Integer, ForeignKey("learners.id"))
