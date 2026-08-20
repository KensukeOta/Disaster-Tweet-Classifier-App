from pathlib import Path

import pytest

from ..app.services.model_service import (
    ModelService,
)


def test_mean_probability():
    probabilities = [
        0.10,
        0.20,
        0.30,
        0.40,
        0.50,
    ]

    result = ModelService._mean_probability(probabilities)

    assert result == pytest.approx(0.30)


def test_mean_probability_rejects_empty_list():
    with pytest.raises(ValueError):
        ModelService._mean_probability([])


def test_classify_as_disaster_at_threshold():
    service = ModelService(
        model_root=Path("."),
        threshold=0.49,
    )

    assert service._classify(0.49) == "disaster"


def test_classify_as_non_disaster_below_threshold():
    service = ModelService(
        model_root=Path("."),
        threshold=0.49,
    )

    assert service._classify(0.489) == "not_disaster"
