from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="Disaster Tweet Classifier API",
    version="0.1.0",
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


class PredictRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=1000,
    )


class PredictResponse(BaseModel):
    prediction: str
    probability: float
    threshold: float


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }


@app.post(
    "/api/v1/predict",
    response_model=PredictResponse,
)
def predict(
    request: PredictRequest,
):
    return PredictResponse(
        prediction="disaster",
        probability=0.75,
        threshold=0.49,
    )
