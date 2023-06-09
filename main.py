from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from api.general_pages.route_homepage import general_pages_router
from db.session import engine   
from db.base import Base 
from api.base import api_router


def include_router(app):
    app.include_router(api_router)

def configure_static(app):
    app.mount("/static", StaticFiles(directory = "static"), name = "static")

def create_tables():           
	Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title = settings.PROJECT_NAME, version = settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app

app = start_application()

# @app.get("/")
# def hello_api():
#     return {"msg": "Hello my API"}
