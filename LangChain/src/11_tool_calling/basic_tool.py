import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))


from langchain_core.tools import Tool


def get_mcu_weather(city : str) -> str:

    """
    Returns a simple weather report for a city
    """

    if city.lower() == "wakanda":
        return f"The weather in {city} is sunny with a temprature of 28 degree celcius"
    elif city.lower() == "sokovia":
        return f"The weather in {city} is cold with a temprature of 4 degree celcius"
    else:
        return f"The weather in {city} is pleasent with a temprature of 20 degree celcius"


def main():

    """
    Demonstrates creating and invoking a baisc LangChain Tool
    """

    weather_tool = Tool(
        name = "get_mcu_weather",
        func = get_mcu_weather,
        description = "Get the current weather information for a city"
    )

    city = "wakanda"

    result = weather_tool.invoke(city)

    print(result)

if __name__ == "__main__":
    main()