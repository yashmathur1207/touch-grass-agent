import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

class OutdoorScout:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY", "")

    def find_nearby_green_spaces(self, location: str = "Indore, Madhya Pradesh") -> list:
        """
        Queries Google Maps / Local search via SerpApi to discover 
        nearby parks, walking trails, and botanical gardens.
        """
        if not self.api_key or self.api_key == "your_serpapi_key_here":
            # Graceful fallback mock if API key is pending
            return [
                {"name": "Meghdoot Upvan", "type": "Public Garden & Park", "address": "Vijay Nagar"},
                {"name": "Pipliyapala Regional Park", "type": "Lake & Nature Park", "address": "Pipliya Pala"},
                {"name": "Nehru Park", "type": "City Green Space", "address": "Shivaji Nagar"}
            ]

        params = {
            "engine": "google_maps",
            "q": f"parks and gardens in {location}",
            "type": "search",
            "api_key": self.api_key,
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            local_results = results.get("local_results", [])
            
            green_spaces = []
            for place in local_results[:3]:
                green_spaces.append({
                    "name": place.get("title"),
                    "type": place.get("type", "Park"),
                    "address": place.get("address", "")
                })
            return green_spaces if green_spaces else [
                {"name": "Local Neighborhood Park", "type": "Park", "address": location}
            ]
        except Exception as e:
            print(f"[SerpApi Error]: {e}")
            return [{"name": "Meghdoot Garden", "type": "Park", "address": location}]

    def get_weather_conditions(self, location: str = "Indore") -> str:
        """
        Checks local weather to include in the intervention briefing.
        """
        if not self.api_key or self.api_key == "your_serpapi_key_here":
            return "Clear skies, mild temperature"

        params = {
            "engine": "google",
            "q": f"weather in {location}",
            "api_key": self.api_key,
        }

        try:
            search = GoogleSearch(params)
            res = search.get_dict()
            weather_box = res.get("weather_result", {})
            temp = weather_box.get("temperature", "26")
            unit = weather_box.get("unit", "°C")
            condition = weather_box.get("condition", "Partly Cloudy")
            return f"{temp} {unit}, {condition}"
        except Exception:
            return "Clear skies, pleasant breeze"

if __name__ == "__main__":
    scout = OutdoorScout()
    print("Finding green spaces...")
    places = scout.find_nearby_green_spaces("Indore")
    for idx, p in enumerate(places, 1):
        print(f"{idx}. {p['name']} ({p['type']}) - {p['address']}")
    
    weather = scout.get_weather_conditions("Indore")
    print(f"\nCurrent Weather: {weather}")