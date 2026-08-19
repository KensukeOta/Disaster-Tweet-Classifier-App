from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)

from .schemas.prediction import (
    PredictRequest,
    PredictResponse,
)
from .services.model_service import (
    ModelService,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_ROOT = PROJECT_ROOT / "models"

model_service = ModelService(
    model_root=MODEL_ROOT,
    threshold=0.49,
    max_length=128,
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    model_service.load()

    yield


app = FastAPI(
    title=("Disaster Tweet Classifier API"),
    version="0.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "models_loaded": len(model_service.models),
    }


@app.post(
    "/api/v1/predict",
    response_model=PredictResponse,
)
def predict(
    request: PredictRequest,
):
    result = model_service.predict(request.text)

    return PredictResponse(
        prediction=result["prediction"],
        probability=result["probability"],
        threshold=result["threshold"],
    )
