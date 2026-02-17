from app.memory.store import memory_store

def get_memory(user_id: str) -> dict:
    return memory_store.get(user_id)

def update_memory(user_id: str, data: dict):
    current = memory_store.get(user_id)
    current.update(data)
    memory_store.set(user_id, current)
