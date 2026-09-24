# API Documentation

Base URL: `http://127.0.0.1:8000`

Interactive OpenAPI reference: `/docs`. Alternative schema: `/redoc`.

## `GET /health`

Returns `{ "status": "ok", "ai_live": true }`.

## `POST /qa`

Request: `{ "text": "What is the largest ocean?" }`

Response: `{ "answer": "..." }`

## `POST /explain`

Request: `{ "topic": "photosynthesis" }`

Response: `{ "topic": "photosynthesis", "explanation": "..." }`

## `POST /summarize`

Request: `{ "text": "A long passage..." }`

Response: `{ "summary": "..." }`

## `POST /quiz`

Request: `{ "text": "The Pythagorean theorem" }`

Response: `{ "quiz": [{ "question": "...", "options": ["..."], "answer": "..." }] }`.

The endpoint expects exactly four options per question from the model. Invalid model JSON returns HTTP 502.

## `POST /learn/recommendations`

Request: `{ "topic": "SQL" }`

Response: `{ "topic": "SQL", "recommendation": "..." }`

All text fields are validated and limited in length. Invalid requests return HTTP 422.
