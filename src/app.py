import os
import pickle
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "data" / "markov_model.pkl"
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

app = FastAPI(title="Balen Bolcha API")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run: uv run python -m src.train_markov"
        )

    with MODEL_PATH.open("rb") as file:
        return pickle.load(file)


generator = load_model()


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_exists": MODEL_PATH.exists(),
    }


@app.get("/api/generate")
def generate(
    paragraphs: int = Query(default=3, ge=1, le=10),
    length: str = Query(default="medium", pattern="^(short|medium|long|extra_long)$"),
):
    text = generator.generate(
        paragraphs=paragraphs,
        length=length,
    )

    return {
        "paragraphs": paragraphs,
        "length": length,
        "text": text,
    }


if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_react_app(full_path: str):
        index_file = FRONTEND_DIST / "index.html"
        return FileResponse(index_file)