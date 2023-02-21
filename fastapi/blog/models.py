from database import Base
from sqlalchemy import Column, Integer, String

class Blog(Base): # this class is extended base from database
    __tablename__ = "blogs"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(18))
    body = Column(String(18))