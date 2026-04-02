Prediction App Setup Guide
This guide will help you set up and run both the backend (FastAPI) and frontend (Flutter) for the Prediction App.

Mission and Problem (4 lines max)
[INSERT YOUR MISSION IN 1-2 LINES]
[INSERT THE SPECIFIC PROBLEM YOUR MODEL SOLVES]
[INSERT WHY THIS MATTERS IN YOUR CONTEXT]
[CONFIRM THIS IS A NON-HOUSING REGRESSION USE CASE]

Dataset Description and Source
Dataset used: `linear_regression/data/upwork_jobs_sample.csv`
Original source: [INSERT DATASET SOURCE LINK]
Dataset summary: [INSERT 1-2 LINES ABOUT COLUMNS/VOLUME/WHY IT FITS REGRESSION]

Prerequisites
Before you begin, make sure you have the following installed on your machine:

- Python 3.x
- pip (Python package manager)
- Flutter SDK
- Android Studio or any preferred IDE for Flutter development (for example, Visual Studio Code)
- A running local network for API communication between the app and the backend (for physical device testing)

1. Clone the repository
Clone the repository to your local machine:

`git clone [INSERT YOUR GITHUB REPO LINK]`
`cd [INSERT YOUR REPO FOLDER NAME]`

2. Set up a Python virtual environment
Create a virtual environment to isolate your project dependencies:

`python -m venv venv`

Activate the virtual environment:

Windows:
`venv\Scripts\activate`

Mac/Linux:
`source venv/bin/activate`

3. Install backend dependencies
Install the required dependencies for the FastAPI backend:

`pip install -r api/requirements.txt`

4. Set up the Model Path
This project already resolves model paths relative to the repository structure.
Saved models are expected under:

`linear_regression/saved_models/`

If you move model files, update paths inside:

`api/main.py`

5. Run the FastAPI server
Start the FastAPI server by running the following command:

`uvicorn api.main:app --reload --host 127.0.0.1 --port 8000`

You should now have the API server running at:

`http://127.0.0.1:8000`

6. Test the API connection (Swagger UI)
Open this in your browser:

`http://127.0.0.1:8000/docs`

This displays Swagger UI where you can test:
- `POST /predict`
- `POST /retrain`
- `GET /health`

7. Install Flutter
Follow the official installation guide for Flutter:

[INSERT FLUTTER INSTALLATION LINK]

8. Prepare Flutter project
From the repo root, move into the Flutter app directory:

`cd FlutterApp`

9. Install Flutter dependencies
Install the required dependencies for the Flutter app:

`flutter pub get`

10. Update the API URL in Flutter
This project uses a build-time variable for API URL.
Run with local API:

`flutter run --dart-define=API_BASE=http://127.0.0.1:8000`

Run with deployed API:

`flutter run --dart-define=API_BASE=[INSERT DEPLOYED API BASE URL]`

11. Run the Flutter app
Run the Flutter app on an emulator or connected device:

`flutter run`

Required Submission Links
GitHub Repository:
[INSERT GITHUB REPO LINK]

Public Swagger UI URL:
[INSERT PUBLIC SWAGGER DOCS LINK]  (example: `https://your-service.onrender.com/docs`)

Public Predict Endpoint URL:
[INSERT PUBLIC PREDICT ENDPOINT LINK]  (example: `https://your-service.onrender.com/predict`)

Video Demo (max allowed by your instructor):
[INSERT YOUTUBE OR VIMEO LINK]

Project Evidence Map
Notebook: `linear_regression/multivariate_fixed.ipynb`
Prediction script: `linear_regression/predict_job_budget.py`
API app: `api/main.py`
Flutter screen: `FlutterApp/lib/main.dart`
Saved model artifacts: `linear_regression/saved_models/`

Notes for Grading
- This project includes Linear Regression, Decision Tree, Random Forest, and SGD (gradient-descent-based) training code.
- The API validates input using Pydantic and includes CORS middleware configuration.
- The `/retrain` endpoint provides a trigger to update model artifacts when new data is supplied.
