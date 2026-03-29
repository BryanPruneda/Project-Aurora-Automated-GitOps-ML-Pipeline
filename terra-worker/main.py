import requests
import time
import redis
import os

# Connect to Redis using the K8s service name
r = redis.Redis(host='aurora-redis-service', port=6379, db=0)

print("--- Texas Soil Monitor: Database Mode ---", flush=True)

while True:
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=32.7555&longitude=-97.3308&hourly=soil_temperature_6cm"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            temp = response.json()['hourly']['soil_temperature_6cm'][0]
            # Save to Redis with a key
            r.set('texas_soil_temp', temp)
            print(f"✅ Saved to DB | Temp: {temp}°C", flush=True)
            time.sleep(60)
        else:
            time.sleep(30)
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        time.sleep(10)
