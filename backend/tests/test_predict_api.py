from fastapi.testclient import TestClient

from ..app.main import app


def test_predict_disaster_tweet():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={"text": ("Forest fire near La Ronge Sask. Canada")},
        )

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == "disaster"

    assert 0.0 <= data["probability"] <= 1.0

    assert data["threshold"] == 0.49


def test_predict_non_disaster_tweet():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={"text": ("I had a great lunch with my friends today!")},
        )

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == "not_disaster"

    assert 0.0 <= data["probability"] <= 1.0

    assert data["threshold"] == 0.49


# 空文字をテスト
def test_predict_rejects_empty_text():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={"text": ""},
        )

    assert response.status_code == 422


def test_predict_requires_text():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={},
        )

    assert response.status_code == 422


# 1000文字超過をテスト
def test_predict_rejects_text_over_1000_characters():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={"text": "a" * 1001},
        )

    assert response.status_code == 422
