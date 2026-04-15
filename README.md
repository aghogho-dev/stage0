# Stage 0 Backend: Name Classification API

A FastAPI-based microservice that integrates with the Genderize API to provide processed gender classification data with confidence scoring.

## Public API URL

[Insert your Railway/Vercel URL here, e.g., https://your-app.up.railway.app]

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **HTTP Client:** HTTPX (Asynchronous)
- **Deployment:** Railway / Vercel

## API Specification

### GET `/api/classify`

Takes a name and returns gender statistics.

**Parameters:**

- `name` (required): The name to classify.

**Success Response (200 OK):**

```json
{
  "status": "success",
  "data": {
    "name": "peter",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-15T16:00:00Z"
  }
}
```
