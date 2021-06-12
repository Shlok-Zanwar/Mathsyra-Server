from fastapi import FastAPI, Request, Body, Query
from Router import router_user
from Database import models, database
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
models.Base.metadata.create_all(database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(router_user.router)


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
