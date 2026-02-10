import re

def can_handle(text: str) -> bool:
    return bool(re.search(r"\d", text)) and any(op in text for op in ["+", "-", "*", "/", "add", "subtract", "multiply", "divide"])

def solve(text: str) -> str:
    try:
        text = text.lower()
        text = text.replace("add", "+").replace("subtract", "-")
        text = text.replace("multiply", "*").replace("divide", "/")
        text = text.replace("by", "")

        expression = re.findall(r"[0-9\+\-\*\/\.\(\)\s]+", text)[0]
        result = eval(expression)

        return f"The answer is {result}"
    except Exception:
        return "I tried to calculate that but got confused 🤔"
