from backend.services.ai.learning.quiz_generator_service import generate_quiz_from_lesson as _generate_from_video


def generate_quiz_from_lesson(video_id):
    """
    Compatibility wrapper for existing imports.
    Returns question dictionaries shaped for admin quiz creation.
    """
    generated = _generate_from_video(video_id)
    output = []
    for item in generated:
        options = item.get("options", [])
        answer = item.get("correct_answer", "")
        option_map = {
            "A": options[0] if len(options) > 0 else "",
            "B": options[1] if len(options) > 1 else "",
            "C": options[2] if len(options) > 2 else "",
            "D": options[3] if len(options) > 3 else "",
        }
        correct_key = "A"
        for key, value in option_map.items():
            if value == answer:
                correct_key = key
                break
        output.append(
            {
                "question_text": item.get("question", ""),
                "option_a": option_map["A"],
                "option_b": option_map["B"],
                "option_c": option_map["C"],
                "option_d": option_map["D"],
                "correct_answer": correct_key,
            }
        )
    return output
