from fastapi import FastAPI, Request, Cookie
from fastapi.staticfiles import StaticFiles
# from fastapi.routing import APIRoute
# from starlette.requests import Request

from routes import route_user, route_category, route_sub_category, route_all_category, route_websocket
from database.model import Base
from database.database import engine
from routes.route_logger_middleware import logger_middleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return {"message": "Hello from FastAPI!"}

app.include_router(route_user.router)
app.include_router(route_category.router)
app.include_router(route_sub_category.router)
app.include_router(route_all_category.router)
app.include_router(route_websocket.router)


app.middleware('http')(logger_middleware)


