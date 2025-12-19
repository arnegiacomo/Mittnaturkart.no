from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routes.observations import router as observations_router
from pathlib import Path

def get_version():
    version_file = Path(__file__).parent.parent / "VERSION"
    if not version_file.exists():
        version_file = Path(__file__).parent.parent.parent / "VERSION"
    try:
        return version_file.read_text().strip()
    except FileNotFoundError:
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
app.include_router(api_v1_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Mittnaturkart API", "version": VERSION}

@app.get("/health")
def health_check():
    return {"status": "ok"}
