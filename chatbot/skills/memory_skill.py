import re
from app.memory.interface import get_memory, update_memory


def can_handle(text: str) -> bool:

    text_lower = text.lower()

    triggers = [
        "remember",
        "what is my",
        "who am i",
        "what do you know about me",
        "do you know about me",
        "which language do i like",
        "what language do i like",
        "favorite language",
    ]

    return any(trigger in text_lower for trigger in triggers)



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
    
    # LIST ALL MEMORY
    if "what do you know about me" in text_lower:

        memory = get_memory(user_id)

        if not memory:
            return "I don't know anything about you yet."

        facts = []

        for key, value in memory.items():
            facts.append(f"Your {key} is {value}")

        return ". ".join(facts) + "."


    # FLEXIBLE LANGUAGE RECALL
    if "language" in text_lower and ("like" in text_lower or "favorite" in text_lower):

        memory = get_memory(user_id)

        if "favorite language" in memory:
            return f"Your favorite language is {memory['favorite language']}."


    # STANDARD RECALL
    if text_lower.startswith("what is my"):

        key = text_lower.replace("what is my", "").strip()

        memory = get_memory(user_id)

        if key in memory:
            return f"Your {key} is {memory[key]}."

        return f"I don't know your {key} yet."

    return None
