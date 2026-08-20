from unittest.mock import patch

from fastapi.testclient import TestClient

from ..app.main import app, model_service


# /healthへアクセスしたとき、
# APIが正常状態とロード済みモデル数を返すことを確認する
def test_health_check():
    original_models = model_service.models

    try:
        model_service.models = [
            object(),
            object(),
            object(),
            object(),
            object(),
        ]

        with (
            patch.object(
                model_service,
                "load",
            ),
            TestClient(app) as client,
        ):
            response = client.get("/health")

        assert response.status_code == 200

        assert response.json() == {
            "status": "ok",
            "models_loaded": 5,
        }

    finally:
        model_service.models = original_models
