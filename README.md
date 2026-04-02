# Upwork Budget Prediction (Linear Regression Summative)

## Mission (4 lines)
Freelancers and hiring teams often struggle to estimate a realistic project budget from job text.
This project predicts expected job budget from title + description features in freelance postings.
The objective is to reduce pricing guesswork and support faster proposal and screening decisions.
It is a non-generic, non-housing regression use case tied to freelance marketplace operations.

## Dataset
- Source dataset used in this repo: `linear_regression/data/upwork_jobs_sample.csv`
- Source type: freelance job postings with budget and hourly signals (prepared for regression training)
- Main fields: `budget`, `hourly_low`, `hourly_high`, `title`, `description`, `country`, `published_date`
- Target: continuous budget value (`budget`, with hourly midpoint fallback during preprocessing)

## Repository Structure
- Notebook: `linear_regression/multivariate_fixed.ipynb`
- Saved models and metrics: `linear_regression/saved_models/`
- API: `api/main.py`
- API compatibility entrypoint: `api/prediction.py`
- Flutter app: `FlutterApp/lib/main.dart`

## Task 1 Evidence (Modeling)
- Regression models implemented in notebook: Linear Regression, Decision Tree, Random Forest, SGD (gradient descent)
- Feature engineering and preprocessing included: missing handling, text feature generation, numeric conversion, scaling/standardization
- Visualizations included (saved in `linear_regression/`):
  - `correlation_heatmap.png`
  - `features_distribution.png`
  - `loss_curves.png` and `sgd_loss_curve.png`
  - `before_after_regression.png` and `regression_line_plot.png`
- Best model persisted to `linear_regression/saved_models/`
- One-point prediction script: `linear_regression/predict_job_budget.py`

## Task 2 Evidence (FastAPI)
- Prediction endpoint: `POST /predict`
- Retraining endpoint: `POST /retrain` (triggers model refresh when new dataset path/rows are provided)
- Health endpoint: `GET /health`
- Swagger UI: `/docs`
- CORS middleware configured in `api/main.py` with explicit origins and methods
- Pydantic validation included for payload data types and range/length constraints

## Public Deployed API (Render)
- Swagger URL: `https://<your-render-service>.onrender.com/docs`
- Prediction URL: `https://<your-render-service>.onrender.com/predict`

Replace `<your-render-service>` with your actual deployed service name before submission.

## Task 3 Evidence (Flutter)
- Single-page mobile UI implemented in `FlutterApp/lib/main.dart`
- Required elements present:
  - Input text fields (title, description)
  - `Predict` button
  - Result/error display area
- API base URL set with build-time define:
  - `flutter run --dart-define=API_BASE=https://<your-render-service>.onrender.com`

## Task 4 Video Demo
- Demo link: https://vimeo.com/1172658333/f1f7bee422
- In demo, ensure you show:
  - Mobile app making predictions
  - Swagger tests for datatype/range validation
  - Notebook model comparison and loss explanation
  - Retraining flow (`/retrain`) for new data updates

## Local Run Instructions
1. Create and activate a Python virtual environment.
2. Install API dependencies:
   - `pip install -r api/requirements.txt`
3. Run API:
   - `uvicorn api.main:app --reload --host 127.0.0.1 --port 8000`
4. Open Swagger:
   - `http://127.0.0.1:8000/docs`
5. Run Flutter app:
   - `cd FlutterApp`
   - `flutter pub get`
   - `flutter run --dart-define=API_BASE=http://127.0.0.1:8000`

## Submission Checklist
- GitHub repo contains notebook, API, Flutter app
- README includes mission, dataset/source, API URL/docs, video link, and app run steps
- Public API URL is routable (not localhost)
- Swagger endpoint is reachable and testable by graders
