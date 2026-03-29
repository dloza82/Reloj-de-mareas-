import requests
import json
from datetime import datetime, timedelta, timezone

# Puerto de Gijón en la API del IHM
PUERTO_ID = 1240

def get_tides_for_date(date_str):
    """Obtiene las mareas del IHM para una fecha dada (YYYYMMDD)"""
    url = f"http://ideihm.covam.es/api-ihm/getmarea?REQUEST=gettide&ID={PUERTO_ID}&date={date_str}&format=json"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if "mareas" in data:
            return data["mareas"]
    except Exception as e:
        print(f"Error fetching {date_str}: {e}")
    return []

# Obtener mareas para hoy, mañana y pasado mañana
now_utc = datetime.now(timezone.utc)
mareas = []

for i in range(3):
    d = now_utc + timedelta(days=i)
    date_str = d.strftime("%Y%m%d")
    print(f"Fetching tides for {date_str}...")
    day_tides = get_tides_for_date(date_str)
    mareas.extend(day_tides)

# Filtrar solo pleamares y bajamares (extremos)
# La API del IHM devuelve datos horarios, buscamos los extremos
extremes = []
if len(mareas) > 2:
    for i in range(1, len(mareas) - 1):
        try:
            h_prev = float(mareas[i-1]["altura"])
            h_curr = float(mareas[i]["altura"])
            h_next = float(mareas[i+1]["altura"])
            
            if h_curr > h_prev and h_curr > h_next:
                extremes.append({
                    "fecha": mareas[i]["fecha"],
                    "altura": h_curr,
                    "tipo": "High"
                })
            elif h_curr < h_prev and h_curr < h_next:
                extremes.append({
                    "fecha": mareas[i]["fecha"],
                    "altura": h_curr,
                    "tipo": "Low"
                })
        except (KeyError, ValueError):
            continue

result = {
    "updated": now_utc.isoformat(),
    "puerto": "Gijon",
    "extremes": extremes
}

with open("mareas.json", "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"Done! Found {len(extremes)} extremes")
print(json.dumps(result, indent=2, ensure_ascii=False))
