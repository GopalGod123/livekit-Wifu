import logging
import os  # ✅ Missing import
from livekit.agents import function_tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun

@function_tool(name="get_weather", description="Get the weather for a given city")
async def get_weather(city: str) -> str:
    """Get the weather for a given city"""
    try:
        # ✅ Fixed API key access - use proper env variable name
        api_key = os.getenv('OPENWEATHER_API_KEY')  # ✅ Proper env var name
        if not api_key:
            return "Weather API key not configured"
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"Weather in {city}: {temp}°C, {description}"
        else:
            return f"Could not get weather for {city}"
    except Exception as e:
        return f"Error getting weather: {str(e)}"

@function_tool(name="search_web", description="Search the web for a given query")
async def search_web(query: str) -> str:
    """Search the web for a given query"""
    try:
        search = DuckDuckGoSearchRun()  # ✅ Create instance first
        result = search.run(query)  # ✅ Use run() method
        return result
    except Exception as e:
        return f"Search error: {str(e)}"
