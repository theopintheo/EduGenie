from ai_service import ai_service


def summarize_text(text: str) -> str:
    prompt = f"Summarize the following passage in plain language. Keep the main ideas and use short paragraphs.\n\n{text}"
    return ai_service.generate(prompt)
