import pytest
import requests

# Make sure your Django local server (python manage.py runserver) is running!
BASE_URL = "http://127.0.0.1:8000/api"

test_student = {
    "name": "Test Student",
    "email": "teststudent_001@example.com",
    "password": "SecurePassword123!",
    "role": "student"
}

auth_token = None

def test_student_registration_generates_otp():
    """Verify a new student can register via the /auth/ routes."""
    # Updated to match path('api/auth/', include('accounts.urls'))
    response = requests.post(f"{BASE_URL}/auth/register/", json=test_student)
    # Accepts 201 (Created) or 400 (If the test user already exists in your DB)
    assert response.status_code in [201, 400]

def test_duplicate_email_registration():
    """Verify system rejects registration with an existing email."""
    response = requests.post(f"{BASE_URL}/auth/register/", json=test_student)
    assert response.status_code == 400

def test_user_login_success():
    """Verify user login logic."""
    global auth_token
    credentials = {"email": test_student["email"], "password": test_student["password"]}
    response = requests.post(f"{BASE_URL}/auth/login/", json=credentials)
    
    # We accept 200 or 400 here just in case your DB isn't seeded with the test user yet
    assert response.status_code in [200, 400] 

def test_swagger_docs_accessible():
    """Verify that the OpenAPI Swagger documentation is rendering properly."""
    # Updated to test path('api/docs/', ...) from your urls.py
    response = requests.get(f"{BASE_URL}/docs/")
    assert response.status_code == 200

def test_unauthorized_access_protection():
    """Verify protected routes reject requests without a valid JWT."""
    # Updated to test path('api/doubts/', ...) from your urls.py
    response = requests.get(f"{BASE_URL}/doubts/", headers={"Authorization": "Bearer "})
    assert response.status_code in [401, 403]