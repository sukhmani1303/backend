from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str




## for response model which is totally new :
class ShowBlog(BaseModel):
    # DM is only title
    title: str
    class Config():
        orm_mode = True

'''

## for response model which inherits DM 
class ShowBlog(Blog):
    # DM are :
    # title and body
    class Config():
        orm_mode = True
        
'''
