from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

## for relationships :
from sqlalchemy.orm import relationship

class Blog(Base): # this class is extended base from database
    __tablename__ = "blogs"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(18))
    body = Column(String(18))

    # as id column of users table is PK, we can create a new column which will be FK
    user_id = Column(Integer ,ForeignKey("users.id"))


    # <name1> = relationship('<class2>', back_populates = '<name2>')
    creator = relationship("User", back_populates="blogs")

## Table for User

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(25))
    password = Column(String(70))
    email = Column(String(50))

    # <name2> = relationship('<class1>', back_populates = '<name1>')
    blogs = relationship("Blog", back_populates="creator")