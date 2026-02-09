from typing import Dict

user_memory: Dict[str, dict] = {}

def get_memory(user_id: str) -> dict:
    return user_memory.get(user_id, {})

def update_memory(user_id: str, data: dict):
    user_memory[user_id] = data
