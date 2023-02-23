### New runner file for routing 

from fastapi import FastAPI
import uvicorn
from main.database import engine
from routers import r_blog,r_user
from main import models

app = FastAPI()
models.Base.metadata.create_all(engine)


app.include_router(r_blog.router)
app.include_router(r_user.router)


if __name__ == '__main__':
    uvicorn.run(app, host = "127.0.0.1", port = 8050)

