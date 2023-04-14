import json
import requests
from SC2006_Project.settings import GOOGLE_API_KEY as GOOGLE_API_KEY
API_KEY = GOOGLE_API_KEY

def get_nearest_carparks(lat, lon, api_key):
    try:
        base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        query = f"location={lat},{lon}&radius=1000&type=parking&key={api_key}"
        url = f"{base_url}{query}"
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            nearest_carparks = data['results']  # Get all the carparks
            return nearest_carparks
        else:
            return []
    except json.JSONDecodeError:
        print("Error parsing JSON response from Google Maps API")
        return []
    except Exception as e:
        print("Error occurred while fetching nearest carparks:", e)
        return []