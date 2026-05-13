from pathlib import Path

import joblib


MODEL_PATH = (
    Path(__file__).resolve().parents[2] / "models" / "disaster_tweet_pipeline.joblib"
)

pipeline = joblib.load(MODEL_PATH)

THRESHOLD = 0.5


def predict_disaster(text: str) -> dict:
    probability = pipeline.predict_proba([text])[0][1]
    prediction = int(probability >= THRESHOLD)

    label = "disaster" if prediction == 1 else "not_disaster"

    return {
        "label": label,
        "prediction": prediction,
        "probability": round(float(probability), 4),
        "threshold": THRESHOLD,
    }
