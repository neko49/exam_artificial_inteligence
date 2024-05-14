import requests
import time

# Récupération des données de qualité de l'air
def get_air_quality_data(city="Paris"):
    api_key = "ef01f6b3a4a88c43c9bed6a9002ffcd155f618b2" 
    url = f"https://api.waqi.info/feed/{city}/"
    params = {
        "token": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        #print(data) 
        if data.get("status") == "ok":
            return data['data']
        else:
            raise Exception(f"Erreur API: {data.get('data', 'unknown error')}")
    else:
        raise Exception("Erreur lors de la récupération des données de qualité de l'air")

# Envoi des données à Logstash
def send_to_logstash(data, logstash_url="http://localhost:5044"):
    import json
    import requests
    headers = {'Content-Type': 'application/json'}
    response = requests.post(logstash_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception("Erreur lors de l'envoi des données à Logstash")

# Exécution du script pour collecter des données en temps réel
if __name__ == "__main__":
    while True:
        try:
            air_quality_data = get_air_quality_data()
            formatted_data = {
                "city": air_quality_data["city"]["name"],
                "aqi": air_quality_data["aqi"],
                "pm25": air_quality_data["iaqi"].get("pm25", {}).get("v", None),
                "pm10": air_quality_data["iaqi"].get("pm10", {}).get("v", None),
                "no2": air_quality_data["iaqi"].get("no2", {}).get("v", None),
                "so2": air_quality_data["iaqi"].get("so2", {}).get("v", None),
                "o3": air_quality_data["iaqi"].get("o3", {}).get("v", None),
                "co": air_quality_data["iaqi"].get("co", {}).get("v", None),
                "timestamp": air_quality_data["time"]["s"]
            }
            send_to_logstash(formatted_data)
            print("Données de qualité de l'air récupérées et envoyées avec succès.")
        except Exception as e:
            print(f"Erreur : {e}")
        time.sleep(3600) 
