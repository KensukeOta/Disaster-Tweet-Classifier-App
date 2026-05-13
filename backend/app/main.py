from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import PredictRequest, PredictResponse
from .services.predictor import predict_disaster
from .config import get_settings

settings = get_settings()

app = FastAPI(title="Disaster Tweet Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Disaster Tweet Classifier API"}


@app.post("/api/v1/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    return predict_disaster(request.text)
