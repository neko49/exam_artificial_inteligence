from elasticsearch import Elasticsearch
import pandas as pd

# Connexion à Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Requête pour obtenir toutes les données de l'index
query = {
    "query": {
        "match_all": {}
    },
    "size": 10000
}

res = es.search(index="air_quality_data", body=query)

# Extraire les données
data = [doc['_source'] for doc in res['hits']['hits']]

# Créer un DataFrame à partir des données
df = pd.json_normalize(data)

# Sauvegarder le DataFrame en fichier CSV
df.to_csv('air_quality_data.csv', index=False)
