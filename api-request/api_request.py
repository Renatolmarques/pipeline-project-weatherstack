# -*- coding: utf-8 -*-
import requests
import json

# --- Real API Call Function ---
def fetch_data():
    """
    Fetches real weather data from the weatherstack API for a hardcoded city.
    """
    print("Fetching weather data from weatherstack API...")
    # NOTE: It's better practice to not hardcode keys in the code.
    # In a real project, this would come from an environment variable.
    api_key = "a508240072260477a9e6bb9bde7aedb5"
    api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=Recife"
    
    try:
        response = requests.get(api_url)
        # This will raise an exception for HTTP error codes (4xx or 5xx)
        response.raise_for_status() 
        print("API response received successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching from API: {e}")
        raise

# --- Mock Data Function for Development ---
def mock_fetch_data():
    """
    Simulates a successful API response to avoid making real calls during development.
    This saves time and prevents exceeding the free tier API limit.
    """
    return {'request': {'type': 'City', 'query': 'Recife, Brazil', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'Recife', 'country': 'Brazil', 'region': 'Pernambuco', 'lat': '-8.050', 'lon': '-34.900', 'timezone_id': 'America/Recife', 'localtime': '2025-07-13 18:12', 'localtime_epoch': 1752430320, 'utc_offset': '-3.0'}, 'current': {'observation_time': '09:12 PM', 'temperature': 26, 'weather_code': 116, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0004_black_low_cloud.png'], 'weather_descriptions': ['Partly cloudy'], 'wind_speed': 16, 'wind_degree': 159, 'wind_dir': 'SSE', 'pressure': 1017, 'precip': 0.4, 'humidity': 79, 'cloudcover': 50, 'feelslike': 29, 'uv_index': 0, 'visibility': 10, 'is_day': 'no'}}