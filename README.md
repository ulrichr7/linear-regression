Prediction App Setup Guide
This guide will help you set up and run both the backend (FastAPI) and frontend (Flutter) for the Prediction App.

Prerequisites
Before you begin, make sure you have the following installed on your machine:

Python 3.x
pip (Python package manager)
Flutter SDK
Android Studio or any preferred IDE for Flutter development (e.g., Visual Studio Code)
A running local network for API communication between the app and the backend.
1. Clone the repository
Clone the repository to your local machine: git clone https://github.com/ulrichr7/linear-regression.git
cd linear-regression

3. Set up a Python virtual environment
Create a virtual environment to isolate your project dependencies: python -m venv venv

Activate the virtual environment:
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

3. Install backend dependencies
Install the required dependencies for the FastAPI backend: pip install -r requirements.txt

4. Set up the Model Path
Ensure the model file model.pkl is available at the correct path. Update the model_path variable in the api.py file if needed: model_path = "C:/Users/kabat/Downloads/model.pkl" # Path to your model

5. Run the FastAPI server
Start the FastAPI server by running the following command: uvicorn api:app --reload --host 192.168.1.82 --port 8000 Note: Make sure 192.168.1.82 is the correct IP address of the machine running the API (this should be accessible from your Flutter app).

You should now have the API server running at http://192.168.1.82:8000.

6. Test the API connection (optional)
You can test the API by navigating to http://192.168.1.82:8000/docs in your browser. This should display the FastAPI Swagger UI where you can test the /predict endpoint.

7. Install Flutter
Follow the official installation guide for Flutter: Flutter Installation.

8. Clone the repository
If you haven't already,
clone the repository for the Flutter frontend: git clone https://github.com/ulrichr7/linear-regression.git
cd Linear-Regression-Model-Deployment-Using-Flutter

10. Install Flutter dependencies
Install the required dependencies for the Flutter app: flutter pub get

11. Update the API URL in main.dart
Make sure the API URL in the main.dart file points to the correct address of your FastAPI backend: final url = 'http://192.168.1.82:8000/predict'; // Replace with your backend address

12. Run the Flutter app
Run the Flutter app on an emulator or connected device: flutter run

Video Demo


Deployed API
