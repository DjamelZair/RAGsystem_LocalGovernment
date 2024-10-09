from elasticsearch import Elasticsearch

# Elasticsearch instellen
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Definieer de index mapping
mapping = {
    "mappings": {
        "properties": {
            "description": {"type": "text"},
            "embedding": {"type": "dense_vector", "dims": 384},  # Voor embeddings
            "Buurtnaam": {"type": "keyword"},
            "Wijknaam": {"type": "keyword"},
            "Stadsdeelnaam": {"type": "keyword"}
        }
    }
}

# Creëer de index 'bouwprojecten'
index_name = 'bouwprojecten'
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)

print("Index 'bouwprojecten' succesvol aangemaakt.")
