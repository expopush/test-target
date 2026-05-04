# Expo Push API Simulator

A stateless mock of the Expo Push API designed for load testing and robustness verification of the `expo-push-starter` library.

## Features
- **Stateless**: Does not store ticket IDs; results are generated randomly based on configuration.
- **Granular Error Control**: Configure the probability of every specific Expo error type via YAML.
- **FastAPI Powered**: Includes a built-in Swagger UI at `/docs`.

## Usage

### Local Execution
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`

### Docker Execution
1. Build: `docker build -t expo-simulator .`
2. Run: `docker run -p 9056:9056 expo-simulator`

## Configuration (`config.yaml`)

Modify `config.yaml` to adjust error rates (values from `0.0` to `1.0`):

- **batch_failures**: HTTP-level failures (401, 429, 500).
- **ticket_errors**: Individual message errors returned in the `/push/send` response.
- **receipt_errors**: Individual receipt errors returned in the `/push/getReceipts` response.
- **missing_percent**: Probability that a receipt is simply omitted from the response map (simulates "not yet ready").

## Endpoints
- `POST /--/api/v2/push/send`: Bulk send notifications.
- `POST /--/api/v2/push/getReceipts`: Bulk fetch delivery receipts.
- `GET /health`: Check simulator status and current configuration.
