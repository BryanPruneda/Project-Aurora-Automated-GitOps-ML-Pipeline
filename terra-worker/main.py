import requests
import time
import os

# Coordinates for Fort Worth/Dallas area
LAT = 32.7555
LON = -97.3308

def fetch_soil_temp():
    # Using Open-Meteo (Free, no API key needed for basic use)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=soil_temperature_6cm"
    try:
        response = requests.get(url)
        data = response.json()
        # Get the latest reading
        current_temp = data['hourly']['soil_temperature_6cm'][0]
        return current_temp
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    print("--- Texas Soil Monitor Active ---")
    while True:
        temp = fetch_soil_temp()
        if temp:
            print(f"Current Soil Temp in Fort Worth: {temp}°C")
        time.sleep(10) # Checks every 10 seconds for now
