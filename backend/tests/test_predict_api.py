from unittest.mock import patch

from fastapi.testclient import TestClient

from ..app.main import app, model_service
from ..app.services.model_service import (
    ModelPrediction,
)


# 災害ツイートを送信したとき、
# 災害判定のレスポンスが正しく返されることを確認する
def test_predict_disaster_tweet():
    prediction = ModelPrediction(
        prediction="disaster",
        probability=0.959192,
        threshold=0.49,
    )

    with (
        patch.object(
            model_service,
            "load",
        ),
        patch.object(
            model_service,
            "predict",
            return_value=prediction,
        ),
        TestClient(app) as client,
    ):
        response = client.post(
            "/api/v1/predict",
            json={"text": ("Forest fire near La Ronge Sask. Canada")},
        )

    assert response.status_code == 200

    assert response.json() == {
        "prediction": "disaster",
        "probability": 0.959192,
        "threshold": 0.49,
    }


# 非災害ツイートを送信したとき、
# 非災害判定のレスポンスが正しく返されることを確認する
def test_predict_non_disaster_tweet():
    prediction = ModelPrediction(
        prediction="not_disaster",
        probability=0.1012,
        threshold=0.49,
    )

    with (
        patch.object(
            model_service,
            "load",
        ),
        patch.object(
            model_service,
            "predict",
            return_value=prediction,
        ),
        TestClient(app) as client,
    ):
        response = client.post(
            "/api/v1/predict",
            json={"text": ("I had a great lunch with my friends today!")},
        )

    assert response.status_code == 200

    assert response.json() == {
        "prediction": "not_disaster",
        "probability": 0.1012,
        "threshold": 0.49,
    }


# 空文字を送信したとき、
# Pydanticの入力バリデーションによって422になることを確認する
def test_predict_rejects_empty_text():
    with (
        patch.object(
            model_service,
            "load",
        ),
        TestClient(app) as client,
    ):
        response = client.post(
            "/api/v1/predict",
            json={
                "text": "",
            },
        )

    assert response.status_code == 422


# textフィールドを送信しなかったとき、
# 必須項目のバリデーションによって422になることを確認する
def test_predict_requires_text():
    with (
        patch.object(
            model_service,
            "load",
        ),
        TestClient(app) as client,
    ):
        response = client.post(
            "/api/v1/predict",
            json={},
        )

    assert response.status_code == 422


# 1000文字を超えるテキストを送信したとき、
# 最大文字数のバリデーションによって422になることを確認する
def test_predict_rejects_text_over_1000_characters():
    with (
        patch.object(
            model_service,
            "load",
        ),
        TestClient(app) as client,
    ):
        response = client.post(
            "/api/v1/predict",
            json={
                "text": "a" * 1001,
            },
        )

    assert response.status_code == 422


# APIへ送信したtextが、
# そのままModelService.predictへ渡されることを確認する
def test_predict_passes_text_to_model_service():
    prediction = ModelPrediction(
        prediction="disaster",
        probability=0.8,
        threshold=0.49,
    )

    with (
        patch.object(
            model_service,
            "load",
        ),
        patch.object(
            model_service,
            "predict",
            return_value=prediction,
        ) as predict_mock,
        TestClient(app) as client,
    ):
        response = client.post(
            "/api/v1/predict",
            json={
                "text": "test tweet",
            },
        )

    assert response.status_code == 200

    predict_mock.assert_called_once_with("test tweet")
