from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)

from .config import (
    CORS_ORIGINS,
    MODEL_MAX_LENGTH,
    MODEL_ROOT,
    MODEL_THRESHOLD,
)
from .schemas.prediction import (
    PredictRequest,
    PredictResponse,
)
from .services.model_service import (
    ModelService,
)

model_service = ModelService(
    model_root=MODEL_ROOT,
    threshold=MODEL_THRESHOLD,
    max_length=MODEL_MAX_LENGTH,
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    model_service.load()

    yield


app = FastAPI(
    title="Disaster Tweet Classifier API",
    version="0.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
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
        prediction=result.prediction,
        probability=result.probability,
        threshold=result.threshold,
    )
