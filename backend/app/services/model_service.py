from dataclasses import dataclass
from pathlib import Path

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


@dataclass(frozen=True)
class ModelPrediction:
    prediction: str
    probability: float
    threshold: float


class ModelService:
    def __init__(
        self,
        model_root: Path,
        threshold: float = 0.49,
        max_length: int = 128,
    ) -> None:
        self.model_root = model_root
        self.threshold = threshold
        self.max_length = max_length

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = None
        self.models = []

    def load(self) -> None:
        tokenizer_path = self.model_root / "tokenizer"

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

        self.models = []

        model_paths = sorted(self.model_root.glob("fold_*"))

        if not model_paths:
            raise RuntimeError("No fold models were found.")

        for model_path in model_paths:
            model = AutoModelForSequenceClassification.from_pretrained(model_path)

            model.to(self.device)

            model.eval()

            self.models.append(model)

        if len(self.models) != 5:
            raise RuntimeError(f"Expected 5 fold models, but found {len(self.models)}.")

    def predict(
        self,
        text: str,
    ) -> ModelPrediction:
        if self.tokenizer is None or not self.models:
            raise RuntimeError("Model is not loaded.")

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_length,
            padding=True,
        )

        inputs.pop(
            "token_type_ids",
            None,
        )

        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        probabilities = []

        with torch.inference_mode():
            for model in self.models:
                outputs = model(**inputs)

                probability = torch.softmax(
                    outputs.logits,
                    dim=-1,
                )[0, 1].item()

                probabilities.append(probability)

        mean_probability = self._mean_probability(probabilities)

        prediction = self._classify(mean_probability)

        return ModelPrediction(
            prediction=prediction,
            probability=mean_probability,
            threshold=self.threshold,
        )

    def _classify(
        self,
        probability: float,
    ) -> str:
        return "disaster" if probability >= self.threshold else "not_disaster"

    @staticmethod
    def _mean_probability(
        probabilities: list[float],
    ) -> float:
        if not probabilities:
            raise ValueError("probabilities must not be empty.")

        return sum(probabilities) / len(probabilities)
