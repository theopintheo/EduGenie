import json
import re
from typing import Any

from ai_service import ai_service


def clean_json_block(text: str) -> str:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    match = re.search(r"\[.*\]", cleaned, flags=re.DOTALL)
    return match.group(0) if match else cleaned


def generate_quiz(text: str) -> list[dict[str, Any]]:
    prompt = f'''Create exactly three quiz multiple-choice questions from this topic: {text}
Return only valid JSON: a list of objects with question, options (exactly four strings), and answer (matching one option).'''
    raw = clean_json_block(ai_service.generate(prompt))
    try:
        quiz = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("The AI returned invalid quiz JSON.") from exc
    if not isinstance(quiz, list):
        raise ValueError("Quiz response must be a list.")
    return quiz
