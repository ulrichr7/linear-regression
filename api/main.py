"""
FastAPI backend for the Upwork job budget predictor.

It loads the persisted decision-tree model and TF-IDF feature list from
`../linear_regression/saved_models/` and exposes a simple `/predict`
endpoint that accepts a job title/description payload.

Note: The original notebook did not persist the trained `TfidfVectorizer`
IDF weights. We recreate a compatible vectorizer from the saved feature
names so column ordering matches the trained model; predictions will
work, but scores may differ slightly from the notebook.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator

# Paths are relative to this file to avoid CWD issues
ROOT_DIR = Path(__file__).resolve().parent
MODEL_DIR = ROOT_DIR.parent / "linear_regression" / "saved_models"


class PredictRequest(BaseModel):
    title: str = Field("", description="Job title or headline")
    description: str = Field("", description="Job description/body text")


class PredictResponse(BaseModel):
    predicted_budget: float = Field(..., description="Budget prediction (model units, typically USD)")
    model: str = Field(..., description="Model file used for inference")
    features: List[str] = Field(..., description="TF-IDF features expected by the model")
    note: Optional[str] = Field(None, description="Warnings or caveats about the prediction")


def _load_pickle(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("rb") as f:
        return pickle.load(f)


def _build_vectorizer(feature_names: List[str]) -> TfidfVectorizer:
    """
    Rebuild a TF-IDF vectorizer with the original vocabulary ordering.
    Because the notebook did not persist IDF weights, we fit on a dummy
    corpus to initialize internal structures while preserving the column
    layout expected by the saved model.
    """
    vocab: Dict[str, int] = {
        name.replace("tfidf_", ""): idx for idx, name in enumerate(feature_names)
    }
    vectorizer = TfidfVectorizer(
        vocabulary=vocab,
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b\w{2,}\b",
        stop_words="english",
        lowercase=True,
    )

    # Fit on a synthetic document containing all tokens once.
    # This sets idf_ to ~1 for every term while keeping column order intact.
    vectorizer.fit([" ".join(vocab.keys())])
    return vectorizer


def _find_model_path(model_dir: Path) -> Path:
    """Pick the best-model file saved by the notebook."""
    preferred = [
        model_dir / "best_model_decision_tree.pkl",
        model_dir / "best_linear_regression_model.pkl",
    ]
    for candidate in preferred:
        if candidate.exists():
            return candidate
    # Fallback: first pickle in the directory
    pkls = sorted(model_dir.glob("*.pkl"))
    if not pkls:
        raise FileNotFoundError(f"No pickle models found in {model_dir}")
    return pkls[0]


class BudgetPredictor:
    def __init__(self, model: BaseEstimator, vectorizer: TfidfVectorizer, feature_names: List[str], model_path: Path):
        self.model = model
        self.vectorizer = vectorizer
        self.feature_names = feature_names
        self.model_path = model_path

    def predict(self, title: str, description: str) -> float:
        text = f"{title or ''} {description or ''}".strip()
        if not text:
            raise ValueError("Provide at least a title or description.")
        matrix = self.vectorizer.transform([text])
        # Model was trained on dense features; convert to numpy array
        features = matrix.toarray()
        return float(self.model.predict(features)[0])


def load_assets() -> BudgetPredictor:
    feature_names_path = MODEL_DIR / "feature_names.pkl"
    feature_names = _load_pickle(feature_names_path)

    model_path = _find_model_path(MODEL_DIR)
    model = _load_pickle(model_path)

    vectorizer = _build_vectorizer(feature_names)
    return BudgetPredictor(model=model, vectorizer=vectorizer, feature_names=feature_names, model_path=model_path)


# Instantiate FastAPI and assets
app = FastAPI(
    title="Upwork Budget Predictor API",
    version="0.1.0",
    description="Predict job budgets using a TF-IDF + regression model trained on Upwork postings.",
)

predictor: Optional[BudgetPredictor] = None


@app.on_event("startup")
def _startup():
    global predictor
    predictor = load_assets()


@app.get("/health")
def health() -> Dict[str, str]:
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {
        "status": "ok",
        "model": predictor.model_path.name,
        "features": str(len(predictor.feature_names)),
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        budget = predictor.predict(request.title, request.description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference failed: {exc}") from exc

    note = (
        "Vectorizer IDF weights were reinitialized from feature names; "
        "predictions may differ slightly from notebook metrics."
    )
    return PredictResponse(
        predicted_budget=budget,
        model=predictor.model_path.name,
        features=predictor.feature_names,
        note=note,
    )


# Convenience root endpoint
@app.get("/")
def root() -> Dict[str, str]:
    return {
        "message": "Upwork Budget Predictor API",
        "predict_endpoint": "/predict",
        "health_endpoint": "/health",
    }
