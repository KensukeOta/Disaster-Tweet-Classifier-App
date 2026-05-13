from fastapi import FastAPI

from .schemas import PredictRequest, PredictResponse
from .services.predictor import predict_disaster

app = FastAPI(title="Disaster Tweet Classifier API")


@app.get("/")
async def root():
    return {"message": "Disaster Tweet Classifier API"}


@app.post("/api/v1/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    return predict_disaster(request.text)
