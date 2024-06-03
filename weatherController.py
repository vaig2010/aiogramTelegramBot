import requests
from keys import weather_key

def getCityWeather(city : str) -> dict:
    api_url = "http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no"
    r = requests.get(api_url.format(weather_key, city)).json()
    if "error" in r:
        return None
    weather = {
        'city' : r["location"]["name"],
        'temperature' : r["current"]["temp_c"],
        'description' : r["current"]["condition"]["text"],
        'icon' : r["current"]["condition"]["icon"]
    }
    return weather
