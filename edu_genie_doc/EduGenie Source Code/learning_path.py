from ai_service import ai_service


def get_learning_recommendations(topic: str) -> str:
    prompt = f"Create a structured learning path for {topic} from beginner to advanced. Include key topics, practice ideas, and resource types."
    return ai_service.generate(prompt)
