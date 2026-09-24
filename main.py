from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from ai_service import ai_service
from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie API", version="1.0.0", description="AI-powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"error": str(exc)})


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12000)


class TopicRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> Any:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"live_ai": ai_service.live},
    )


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"status": "ok", "ai_live": ai_service.live}


@app.post("/qa")
def qa(payload: TextRequest) -> dict[str, str]:
    return {"answer": answer_question(payload.text)}


@app.post("/explain")
def explain(payload: TopicRequest) -> dict[str, str]:
    return {"topic": payload.topic, "explanation": explain_topic(payload.topic)}


@app.post("/summarize")
def summarize(payload: TextRequest) -> dict[str, str]:
    return {"summary": summarize_text(payload.text)}


@app.post("/quiz")
def quiz(payload: TextRequest) -> dict[str, Any]:
    try:
        return {"quiz": generate_quiz(payload.text)}
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations")
def recommendations(payload: TopicRequest) -> dict[str, str]:
    return {"topic": payload.topic, "recommendation": get_learning_recommendations(payload.topic)}
