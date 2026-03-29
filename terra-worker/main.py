import requests
import time
import redis
import json
import psycopg2

r = redis.Redis(host='aurora-redis-service', port=6379, db=0)

# Strategic Texas Hubs
TEXAS_POINTS = {
    "Dallas": (32.77, -96.79), "Fort Worth": (32.75, -97.33),
    "Austin": (30.26, -97.74), "Houston": (29.76, -95.36),
    "San Antonio": (29.42, -98.49), "El Paso": (31.76, -106.48),
    "Amarillo": (35.22, -101.83), "Lubbock": (33.57, -101.85),
    "Corpus Christi": (27.80, -97.39), "Laredo": (27.53, -99.48),
    "Brownsville": (25.90, -97.49), "Midland": (31.99, -102.07),
    "Abilene": (32.44, -99.73), "Tyler": (32.35, -95.30),
    "Beaumont": (30.08, -94.12)
}

print("--- Lone Star Monitor: Full State Mode ---", flush=True)

while True:
    try:
        grid_data = []
        conn = psycopg2.connect(host="aurora-postgres-service", database="postgres", user="postgres", password="fortworth")
        cur = conn.cursor()
        
        for name, coords in TEXAS_POINTS.items():
            lat, lon = coords
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=soil_temperature_6cm"
            res = requests.get(url, timeout=5).json()
            temp = res['hourly']['soil_temperature_6cm'][0]
            
            point = {"lat": lat, "lon": lon, "temp": temp, "id": name}
            grid_data.append(point)
            
            # Save to history
            cur.execute("INSERT INTO soil_history (temp, lat, lon) VALUES (%s, %s, %s)", (temp, lat, lon))
        
        conn.commit()
        cur.close()
        conn.close()
        
        r.set('texas_grid_data', json.dumps(grid_data))
        print(f"✅ State-Wide Sync: {len(grid_data)} hubs updated", flush=True)
        time.sleep(120) 
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        time.sleep(10)
