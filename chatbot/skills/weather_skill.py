import os
import httpx
from dotenv import load_dotenv

load_dotenv(".env")

API_KEY = os.getenv("WEATHER_API_KEY")


def can_handle(text: str) -> bool:
    return "weather in" in text.lower()


async def handle(text: str) -> str:

    if not API_KEY:
        return "Weather API key is missing."

    city = text.lower().split("weather in", 1)[1].strip().title()

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)

        data = response.json()

        if response.status_code != 200:
            print("Weather error:", data)
            return f"I couldn't find weather for {city}."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"The weather in {city} is {desc}, {temp}°C."

    except Exception as e:
        print("Weather exception:", e)
        return "Weather service unavailable."
