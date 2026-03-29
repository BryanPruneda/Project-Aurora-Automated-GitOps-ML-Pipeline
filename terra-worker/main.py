import requests
import time
import redis
import psycopg2

# Connections
r = redis.Redis(host='aurora-redis-service', port=6379, db=0)
conn = psycopg2.connect(host="aurora-postgres-service", database="postgres", user="postgres", password="fortworth")
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("CREATE TABLE IF NOT EXISTS soil_history (ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, temp FLOAT);")
conn.commit()

print("--- Texas Monitor: Triple Threat Mode ---", flush=True)

while True:
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=32.7555&longitude=-97.3308&hourly=soil_temperature_6cm"
        temp = requests.get(url).json()['hourly']['soil_temperature_6cm'][0]
        
        # 1. Update Redis (Now)
        r.set('texas_soil_temp', temp)
        
        # 2. Update Postgres (History)
        cur.execute("INSERT INTO soil_history (temp) VALUES (%s)", (temp,))
        conn.commit()
        
        # 3. Alert Logic
        if temp < 0:
            print(f"❄️ ALERT: FREEZE DETECTED IN FORT WORTH: {temp}°C", flush=True)
        else:
            print(f"✅ Logged {temp}°C to History", flush=True)
            
        time.sleep(60)
    except Exception as e:
        print(f"Error: {e}", flush=True)
        time.sleep(10)
