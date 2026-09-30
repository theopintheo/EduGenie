# Setup Guide

## Prerequisites

- Python 3.10+
- A terminal and VS Code
- Optional: Google AI Studio account and Gemini API key

## Windows setup

```powershell
cd C:\Users\Theopin.B\Desktop\edu_genie
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env`, set `GEMINI_API_KEY`, then run:

```powershell
uvicorn main:app --reload
```

Never paste an API key into source files, chat, screenshots, or Git. If a key is exposed, revoke it in Google AI Studio and create a replacement. For a temporary PowerShell session, you can configure the replacement without writing it to the repository:

```powershell
$env:GEMINI_API_KEY = "paste-your-new-key-here"
$env:GEMINI_MODEL = "antigravity-preview-09-2026"
uvicorn main:app --reload
```

Browse to `http://127.0.0.1:8000`. Use `http://127.0.0.1:8000/docs` to inspect or call endpoints.

## Troubleshooting

- PowerShell blocks activation: run `Set-ExecutionPolicy -Scope Process Bypass` and activate again.
- Demo mode appears: check that `.env` exists beside `main.py` and the key is non-empty, then restart Uvicorn.
- Port in use: run `uvicorn main:app --reload --port 8001`.
- Never commit `.env`; it is ignored by Git.
