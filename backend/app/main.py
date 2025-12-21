from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routes.observations import router as observations_router
from .routes.locations import router as locations_router
from pathlib import Path
import tomllib

def get_version():
    pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
    try:
        with open(pyproject_file, "rb") as f:
            data = tomllib.load(f)
            return data["project"]["version"]
    except (FileNotFoundError, KeyError):
        return "1.0.0"

VERSION = get_version()

app = FastAPI(title="Mittnaturkart API", version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(observations_router)
api_v1_router.include_router(locations_router)
app.include_router(api_v1_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Mittnaturkart API", "version": VERSION}

@app.get("/health")
def health_check():
    return {"status": "ok"}
