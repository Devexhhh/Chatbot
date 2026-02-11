from datetime import datetime

def can_handle(text: str) -> bool:
    text = text.lower()
    return any(phrase in text for phrase in [
        "time", "current time",
        "date", "today", "today's date"
    ])

def handle(text: str) -> str:
    now = datetime.now()

    if "time" in text:
        return f"The current time is {now.strftime('%H:%M:%S')}"

    if "date" in text or "today" in text:
        return f"Today's date is {now.strftime('%Y-%m-%d')}"

    return None
