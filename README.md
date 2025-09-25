# MKVStore

This is a simple key-value store application built with Python, Flask, Redis, and PostgreSQL.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10 or later
- Docker and Docker Compose

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd mkvstore
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the database and Redis services:**
    ```bash
    docker-compose up -d
    ```

2.  **Run the Flask application:**
    ```bash
    python3.10 app.py
    ```

The API will be running at `http://127.0.0.1:5000`.

## API Endpoints


-   **Login:**
    -   METHOD: POST
    -   URL: `/auth/login`
    -   Payload: `{"tenant_name":"tenant1", "password": "pass101" }`
    -   CURL: 
        `curl --location 'http://127.0.0.1:5000/auth/login' \
        --header 'Content-Type: application/json' \
        --data '{
            "tenant_name":"tenant1",
            "password": "pass101"
        }'`
-   **Refresh:**
    -   METHOD: POST
    -   URL: `/auth/refresh`
    -   Payload: `{"refresh_token": "....."}`
    -   CURL:
        `curl --location 'http://127.0.0.1:5000/auth/refresh' \
        --header 'Content-Type: application/json' \
        --data '{
            "refresh_token": "...."
        }'`
-   **Protected Route Example:**
    -   METHOD: GET
    -   URL: `/auth/test_protected`
    -   Header: `{"Authorization": "Bearer ....."}`
    -   CURL: 
        `curl --location 'http://127.0.0.1:5000/auth/test_protected' \ 
        --header 'Authorization: Bearer .....' `
