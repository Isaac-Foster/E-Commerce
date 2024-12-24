
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from ecommerce.config import root_path
from ecommerce.core.models import init_post
from ecommerce.core.interfaces.routers import configure_routes

app = FastAPI()

app.mount("/static", StaticFiles(directory=root_path / "static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_post()
configure_routes(app)
#app.include_router(view.router)
