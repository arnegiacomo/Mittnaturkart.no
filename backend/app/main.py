from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routes.observations import router as observations_router
from .routes.locations import router as locations_router
from .routes.auth import router as auth_router
from .config import settings
from .middleware import LoggingMiddleware
from .logging_context import SubFilter
from pathlib import Path
import tomllib
import logging

def get_version():
    pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
    try:
        with open(pyproject_file, "rb") as f:
            data = tomllib.load(f)
            return data["project"]["version"]
    except (FileNotFoundError, KeyError):
        return "1.0.0"

VERSION = get_version()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [sub=%(sub)s] - %(message)s'
)
for handler in logging.root.handlers:
    handler.addFilter(SubFilter())

app = FastAPI(title="Mittnaturkart API", version=VERSION)

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(observations_router)
api_v1_router.include_router(locations_router)
api_v1_router.include_router(auth_router)
app.include_router(api_v1_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Mittnaturkart API", "version": VERSION}

@app.get("/health")
def health_check():
    return {"status": "ok"}
