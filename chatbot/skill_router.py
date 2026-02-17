import inspect

from chatbot.skills.math_skill import can_handle as can_math, solve as solve_math
from chatbot.skills.time_skill import can_handle as can_time, handle as handle_time
from chatbot.skills.weather_skill import can_handle as can_weather, handle as handle_weather


async def handle_skills(text: str):

    if can_math(text):
        return solve_math(text)

    if can_time(text):
        return handle_time(text)

    if can_weather(text):
        result = handle_weather(text)

        # only await if async
        if inspect.iscoroutine(result):
            return await result

        return result

    return None
