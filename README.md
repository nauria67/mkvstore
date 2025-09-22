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

All endpoints are `POST` requests.

-   **Get a value:**
    -   URL: `/mkv/get`
    -   Payload: `{"tenant": "your_tenant", "key": "your_key"}`
-   **Set a value:**
    -   URL: `/mkv/put`
    -   Payload: `{"tenant": "your_tenant", "key": "your_key", "value": "your_value"}`
-   **Delete a value:**
    -   URL: `/mkv/delete`
    -   Payload: `{"tenant": "your_tenant", "key": "your_key"}`