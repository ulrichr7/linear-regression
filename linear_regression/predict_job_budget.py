"""
Lightweight CLI helper for the Upwork budget predictor model.

Example:
    python predict_job_budget.py --title "Logo design" --description "Need a modern brand mark for a fintech startup."
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make the sibling `api` package importable when run from this directory
SUMMATIVE_DIR = Path(__file__).resolve().parent.parent
if str(SUMMATIVE_DIR) not in sys.path:
    sys.path.insert(0, str(SUMMATIVE_DIR))

from api.prediction import load_assets  # type: ignore


def main() -> int:
    parser = argparse.ArgumentParser(description="Predict Upwork job budget using the saved model.")
    parser.add_argument("--title", default="", help="Job title or headline.")
    parser.add_argument("--description", default="", help="Job description/body text.")
    args = parser.parse_args()

    predictor = load_assets()

    try:
        budget = predictor.predict(args.title, args.description)
    except Exception as exc:  # noqa: BLE001 - surfaced to CLI
        print(f"Prediction failed: {exc}", file=sys.stderr)
        return 1

    print(f"Predicted budget: {budget:.2f}")
    print(f"Model: {predictor.model_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
