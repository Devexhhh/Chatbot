from chatbot.skills.math_skill import can_handle as can_math, solve as solve_math
from chatbot.skills.time_skill import can_handle as can_time, handle as handle_time

def handle_skills(text: str):
    # Math first (more specific)
    if can_math(text):
        return solve_math(text)
    
    # Time/Date
    if can_time(text):
        return handle_time(text)

    return None
