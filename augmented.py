from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

# Load environment variables from .env file
load_dotenv(override=True)

def get_weather(location: str) -> str:
    """
    Get weather information for a given location using Open-Meteo API
    First converts location to coordinates using Nominatim, then gets weather
    """
    # First, get coordinates for the location using Nominatim (OpenStreetMap)
    geocoding_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    try:
        geo_response = requests.get(geocoding_url, headers={'User-Agent': 'WeatherApp/1.0'})
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data:
            return f"Error: Could not find location '{location}'"
        
        # Get coordinates from first result
        lat = float(geo_data[0]['lat'])
        lon = float(geo_data[0]['lon'])
        
        # Get weather data from Open-Meteo
        weather_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "weather_code"],
            "temperature_unit": "fahrenheit",
            "timezone": "auto"
        }
        
        weather_response = requests.get(weather_url, params=params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Get current weather information
        temp = weather_data["current"]["temperature_2m"]
        weather_code = weather_data["current"]["weather_code"]
        
        # Convert weather code to description
        weather_descriptions = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "foggy",
            48: "depositing rime fog",
            51: "light drizzle",
            53: "moderate drizzle",
            55: "dense drizzle",
            61: "slight rain",
            63: "moderate rain",
            65: "heavy rain",
            71: "slight snow fall",
            73: "moderate snow fall",
            75: "heavy snow fall",
            77: "snow grains",
            80: "slight rain showers",
            81: "moderate rain showers",
            82: "violent rain showers",
            85: "slight snow showers",
            86: "heavy snow showers",
            95: "thunderstorm",
            96: "thunderstorm with slight hail",
            99: "thunderstorm with heavy hail",
        }
        
        description = weather_descriptions.get(weather_code, "unknown conditions")
        return f"The current temperature in {location} is {temp}°F with {description}"
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the weather tool
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather information for a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g. 'London' or 'Paris, France'"
                }
            },
            "required": ["location"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

# Initial user message
messages = [{"role": "user", "content": "What's the weather like in Da Nang, Vietnam today?"}]

# Get completion from OpenAI
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

# Handle the function call
if completion.choices[0].message.tool_calls:
    tool_call = completion.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = eval(tool_call.function.arguments)
    
    # Get weather data
    weather_data = get_weather(**function_args)
    
    # Add the assistant's message and function result to the conversation
    messages.append(completion.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": weather_data
    })
    
    # Get final response from OpenAI
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )
    
    print(final_response.choices[0].message.content)
else:
    print(completion.choices[0].message.content)
