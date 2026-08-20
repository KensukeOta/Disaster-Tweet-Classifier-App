# Disaster Tweet Classifier

英語のツイートが実際の災害に関する投稿かどうかを判定するWebアプリケーションです。

Kaggleの「Natural Language Processing with Disaster Tweets」に取り組み、学習したDistilBERTの5-Fold EnsembleモデルをWebアプリとして実装しました。

## Demo

> デプロイ後にURLを追加予定

## Features

- 英語ツイートの災害 / 非災害分類
- 災害確率の表示
- 5つのDistilBERTモデルによる確率平均
- OOFで決定した分類閾値を使用
- サンプルツイートからの判定
- レスポンシブUI
- 入力バリデーション
- APIエラー・タイムアウト処理

## Model

### Architecture

推論にはDistilBERTの5-Fold Ensembleを使用しています。

```text
Tweet
  ↓
Tokenizer
  ↓
┌────────┬────────┬────────┬────────┬────────┐
│ Fold 1 │ Fold 2 │ Fold 3 │ Fold 4 │ Fold 5 │
└────────┴────────┴────────┴────────┴────────┘
  ↓
Probability Average
  ↓
Threshold = 0.49
  ↓
Disaster / Not Disaster
```

各Foldモデルが出力した災害クラスの確率を平均し、その値が0.49以上の場合に`disaster`と判定します。

### Validation

| Metric                    |  Score |
| ------------------------- | -----: |
| 5-Fold Mean F1            | 0.8065 |
| 5-Fold F1 Std             | 0.0071 |
| OOF F1 (threshold = 0.50) | 0.8064 |
| Optimized OOF F1          | 0.8065 |
| Optimized Threshold       |   0.49 |

FoldごとのValidation F1：

| Fold |     F1 |
| ---- | -----: |
| 1    | 0.8079 |
| 2    | 0.8065 |
| 3    | 0.7969 |
| 4    | 0.8167 |
| 5    | 0.8044 |

### Kaggle Result

| Submission                             | Public Score |
| -------------------------------------- | -----------: |
| DistilBERT 5-Fold / threshold 0.50     |      0.83328 |
| DistilBERT 5-Fold / OOF threshold 0.49 |  **0.83389** |

## Experiment History

モデル構築では、古典的なNLP手法からTransformerへ段階的に改善しました。

| Approach                            | Kaggle Public Score |
| ----------------------------------- | ------------------: |
| TF-IDF + Logistic Regression        |             0.79650 |
| Char TF-IDF + Logistic Regression   |             0.80386 |
| Word / Char Ensemble                |             0.81182 |
| FeatureUnion                        |             0.81458 |
| DistilBERT                          |             0.82776 |
| DistilBERT + Threshold Optimization |             0.83113 |
| DistilBERT 5-Fold Ensemble          |         **0.83389** |

## Tech Stack

### Frontend

- SvelteKit
- Svelte 5
- TypeScript
- Tailwind CSS

### Backend

- FastAPI
- Python 3.12
- PyTorch
- Transformers
- uv

### Machine Learning

- DistilBERT
- 5-Fold Ensemble
- Probability Averaging
- Threshold Optimization

## Project Structure

```text
Disaster-Tweet-Classifier-App/
├── frontend/
│   └── src/
│
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── schemas/
│   │   └── services/
│   └── tests/
│
├── models/
│   ├── tokenizer/
│   ├── fold_1/
│   ├── fold_2/
│   ├── fold_3/
│   ├── fold_4/
│   └── fold_5/
│
└── README.md
```

モデルファイルは容量が大きいためGitリポジトリには含めていません。

## Local Development

### Backend

```bash
cd backend
uv sync
uv run fastapi dev app/main.py
```

API:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

### Environment Variables

Frontend:

```env
PUBLIC_API_BASE_URL=http://localhost:8000
```

Backend:

```env
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## API

### POST `/api/v1/predict`

Request:

```json
{
  "text": "Forest fire near La Ronge Sask. Canada"
}
```

Response example:

```json
{
  "prediction": "disaster",
  "probability": 0.959192,
  "threshold": 0.49
}
```

## Test

Backend:

```bash
cd backend
uv run pytest -v
```

Lint:

```bash
uv run ruff check
```

## Disclaimer

このアプリケーションはKaggleのデータセットを使用して作成した機械学習プロジェクトです。

出力は機械学習モデルによる推定結果であり、実際の災害情報や緊急情報の確認を目的としたものではありません。
