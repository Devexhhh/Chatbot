from chatbot.skills.math_skill import can_handle as can_math, solve as solve_math

def handle_skills(text: str):
    if can_math(text):
        return solve_math(text)
    return None
