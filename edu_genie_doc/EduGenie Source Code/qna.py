from ai_service import ai_service


def answer_question(question: str) -> str:
    prompt = f"Answer this learner question accurately and clearly. Mention uncertainty when relevant. Question: {question}"
    return ai_service.generate(prompt)
