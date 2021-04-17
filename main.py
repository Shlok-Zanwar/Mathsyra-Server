from fastapi import FastAPI, Request, Body, Query
from Router import router_user
from Database import models, database


app = FastAPI()
models.Base.metadata.create_all(database.engine)


app.include_router(router_user.router)
