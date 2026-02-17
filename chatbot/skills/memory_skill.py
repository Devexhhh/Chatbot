import re
from app.memory.interface import get_memory, update_memory


def can_handle(text: str) -> bool:
    text = text.lower()
    return (
        text.startswith("remember")
        or text.startswith("what is my")
        or text.startswith("who am i")
    )


async def handle(text: str, user_id: str) -> str:

    text_lower = text.lower()

    # STORE MEMORY
    if text_lower.startswith("remember"):

        match = re.match(r"remember my (.+) is (.+)", text_lower)

        if not match:
            return "Tell me like: remember my name is Devex"

        key, value = match.groups()

        memory = get_memory(user_id)
        memory[key] = value
        update_memory(user_id, memory)

        return f"I'll remember that your {key} is {value}."


    # RECALL MEMORY
    if text_lower.startswith("what is my"):

        key = text_lower.replace("what is my", "").strip()

        memory = get_memory(user_id)

        if key in memory:
            return f"Your {key} is {memory[key]}."

        return f"I don't know your {key} yet."


    # IDENTITY RECALL
    if text_lower.startswith("who am i"):

        memory = get_memory(user_id)

        if "name" in memory:
            return f"You are {memory['name']}."

        return "I don't know your name yet."

    if text_lower == "what do you know about me":

        memory = get_memory(user_id)

        if not memory:
            return "I don't know anything about you yet."

        facts = "\n".join(f"{k}: {v}" for k, v in memory.items())

        return f"Here is what I know about you:\n{facts}"


    return None
