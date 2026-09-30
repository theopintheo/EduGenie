# AI Integration

EduGenie uses the configured `antigravity-preview-09-2026` model through the current `google-genai` SDK. `ai_service.py` loads `GEMINI_API_KEY` and `GEMINI_MODEL` from `.env`, configures the SDK, and exposes one shared `AIService` instance.

Each feature owns its prompt and calls `ai_service.generate()`. This keeps API credentials and provider setup in one place while allowing prompts to evolve independently.

## Model responsibilities

- The configured model: question answering, explanations, summaries, quizzes, and learning paths.
- Demo fallback: deterministic sample output when no key is available, so UI and endpoint work can be developed offline.

## Reliability decisions

- Request models validate empty and oversized input.
- Quiz output is cleaned of Markdown fences and parsed as JSON.
- Empty Gemini responses and malformed quizzes raise useful errors.
- The UI displays API errors instead of silently failing.

## Security and quality

Keep keys in environment variables, never source code. Add rate limiting and authentication before public deployment. Review generated educational material for accuracy, bias, copyright, and age appropriateness. Log request metadata without storing sensitive learner content by default.
