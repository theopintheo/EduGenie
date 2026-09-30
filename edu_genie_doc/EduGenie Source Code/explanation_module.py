from ai_service import ai_service


def explain_topic(topic: str) -> str:
    prompt = f"Explain {topic} for a beginner. Use simple language, one analogy, and three key takeaways."
    return ai_service.generate(prompt)
