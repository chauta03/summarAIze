# SummarAIze Backend

This is the backend service for SummarAIze, a tool that provides meeting summaries and Google Meet integration.

## Requirements

- Python

## Setup

1. Create and activate a virtual environment:

   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

2. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your environment variables:

   ```sh
   touch .env
   ```

4. Add your Google API credentials to `credentials.json`.

## Running the Application

1. Start the FastAPI server:

   ```sh
   fastapi dev main.py
   ```

2. The API will be available at `http://127.0.0.1:8000`.
