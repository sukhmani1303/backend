### Creating an Engine ###

from sqlalchemy import create_engine

# for sqlite local .db file
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog/db' # for sqlite local .db file
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False})

# for connecion in XAMPP
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/blog" 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

### Declaring a Mapping ###

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

### Creating a Session ###

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush = False)