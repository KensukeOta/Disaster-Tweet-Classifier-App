from pathlib import Path

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


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

        for fold_number in range(
            1,
            6,
        ):
            model_path = self.model_root / f"fold_{fold_number}"

            model = AutoModelForSequenceClassification.from_pretrained(model_path)

            model.to(self.device)

            model.eval()

            self.models.append(model)

    def predict(
        self,
        text: str,
    ) -> dict[str, float | str]:
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

        mean_probability = sum(probabilities) / len(probabilities)

        prediction = (
            "disaster" if mean_probability >= self.threshold else "not_disaster"
        )

        return {
            "prediction": prediction,
            "probability": mean_probability,
            "threshold": self.threshold,
        }
