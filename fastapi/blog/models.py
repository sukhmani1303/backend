from database import Base
from sqlalchemy import Column, Integer, String

class Blog(Base): # this class is extended base from database
    __tablename__ = "blogs"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(18))
    body = Column(String(18))

## Table for User

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(25))
    password = Column(String(25))
    email = Column(String(50))