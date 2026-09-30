import os
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None


class AIService:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "antigravity-preview-09-2026")
        self._model: Optional[Any] = None
        if self.api_key and genai:
            self._model = genai.Client(
                api_key=self.api_key,
                http_options={"api_version": "v1", "timeout": 30000},
            )

    @property
    def live(self) -> bool:
        return self._model is not None

    def generate(self, prompt: str) -> str:
        if not self._model:
            demo = self._demo_response(prompt)
            if "quiz" in prompt.lower() or "multiple-choice" in prompt.lower():
                return demo
            return "Demo mode is active. Add GEMINI_API_KEY to .env for a live AI response.\n\n" + demo
        try:
            if self.model_name.startswith("antigravity-"):
                response = self._model.interactions.create(
                    agent=self.model_name,
                    environment={"type": "remote"},
                    input=prompt,
                )
                text = getattr(response, "output_text", "").strip()
            else:
                response = self._model.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
                text = getattr(response, "text", "").strip()
        except Exception as exc:
            demo = self._demo_response(prompt)
            if "quiz" in prompt.lower() or "multiple-choice" in prompt.lower():
                return demo
            return (
                "Live Gemini is unavailable for this project right now. "
                "Showing a local demo response instead.\n\n"
                + demo
            )
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text

    @staticmethod
    def _demo_response(prompt: str) -> str:
        lowered = prompt.lower()
        if "photosynthesis" in lowered:
            return """**Photosynthesis** is the process plants use to convert light energy into chemical energy.

### Main inputs

* **Sunlight**, captured by chlorophyll
* **Carbon dioxide ($CO_2$)** from the air
* **Water ($H_2O$)** absorbed through the roots

### Main outputs

Plants produce **glucose** for energy and release **oxygen ($O_2$)** into the atmosphere.

### Simple equation

$$6CO_2 + 6H_2O + light energy -> C_6H_12O_6 + 6O_2$$"""
        if "season" in lowered:
            return """**Seasons change** because Earth is tilted on its axis as it travels around the Sun.

When a hemisphere tilts toward the Sun, it receives more direct sunlight and longer days, creating **summer**. When it tilts away, it receives less direct sunlight and shorter days, creating **winter**."""
        if "gravity" in lowered:
            return """**Gravity** is the force that attracts objects with mass toward one another.

On Earth, gravity pulls objects toward the ground and keeps the Moon in orbit. The more massive an object is, the stronger its gravitational pull."""
        if "summarize" in lowered:
            return "This is a concise demo summary. The original passage should be reviewed with Gemini enabled for a content-specific result."
        if "quiz" in lowered:
            return '[{"question":"What is the best next step for this topic?","options":["Review the basics","Skip all practice","Avoid examples","Memorize unrelated facts"],"answer":"Review the basics"}]'
        if "learning path" in lowered:
            return "Beginner: learn the vocabulary and core ideas.\nIntermediate: solve guided examples and small exercises.\nAdvanced: build a project, evaluate trade-offs, and teach the concept."
        if "explain" in lowered:
            return "Start with the definition, connect it to a familiar example, then practice it in a small problem."
        return "Ask a focused question and Gemini will provide a learning-oriented answer."


ai_service = AIService()
