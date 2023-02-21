# uvicorn main:app --reload
from fastapi import FastAPI
from typing import Optional
import uvicorn

app = FastAPI()

@app.get('/')
# @app is called path operation decorator
# ('/') is path [ ('/') is index path , generally 8080]
# .get is operation [.post, .put, .delete etc]
# we can have any name to function below (even repeat names)
# the function is called path operation function

def index():
    return {'data' : 'this is index page'}

### dynamic routing ###

# the variable for dynamic routing is written in '{}' and
# can be treated as a variable
# here, id is our variable
# the variable must also be passed in function as arg
@app.get('/show/{id}')
def show_id(id:int):
    return {'id' : id}

#we can have multiple variables in dynamic url
@app.get('/mul/{id1}/{id2}')
# using : <datatype>, one can specify the datatype of arg
def mul(id1 : int,id2 : int):
    return {'mul' : id1*id2}

# The variable can be placed anywhere in the link
@app.get('/blogger/{id}/comments')
def comm_fetch(id):
    return {'comments' : 'fetching the comments of id ' + id}


### Query Parameters ###

# we can use query params with the help of '?'
# we don't have to modify our path but only the 
# args in function

@app.get('/qry_test')
# we can also set default value to avoid error incase
# the value isn't set in url
# We can have multiple query params but not accept all of them
# only the ones passed in the function can be accessed
# we can also save some qry param as optional

def qry_prms(chk: bool = False ,limit = 0, tag = "", sort: Optional[str] = None):
    if chk:
        return {'data' : f'we have set limit to {limit} and tag to {tag}'}
    else:
        return {'data' : 'Cant access data !'}
    

### Request Body ###

# we can test post requests from swagger Docs
# we use request body to send data from client to API
# we use Pydantic models
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

# we have to create an API of our own to manage data
# we create a Class with parameters and its Datatype
# we declare the args in function with Datatype of Class

@app.post('/blog1')
def create_blog(request : Blog): # we can use any name for arg 
    return request

# we can create multiple such classes to return 
# various types of data

class B1(BaseModel):
    a: int

class B2(BaseModel):
    b: int

@app.post('/blog2')
def cr_blog(i1: B1, i2: B2):
    mul1 = i1.a*i2.b # using the '.' operator, we can access the Data Members
    return {"data" : f"the multiplication is {mul1}"}

# runner code
if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 9000)