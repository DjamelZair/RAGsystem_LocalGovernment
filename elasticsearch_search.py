from elasticsearch import Elasticsearch

# Initialiseer Elasticsearch verbinding
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Functie om op basis van tekst te zoeken
def search_with_embeddings(query, index_name='nieuwbouwplannen'):
    # Elasticsearch body voor de tekstuele zoekopdracht
    body = {
        "query": {
            "match": {
                "Stadsdeelnaam": query  # Moet overeenkomen met CSV-bestand
            }
        }
    }

    # Voer de zoekopdracht uit en krijg de resultaten
    result = es.search(index=index_name, body=body)
    return result['hits']['hits']

# Functie voor datumgebaseerde zoekopdrachten
def search_by_date(year, index_name='nieuwbouwplannen'):
    # Elasticsearch body voor datumzoekopdracht
    body = {
        "query": {
            "range": {
                "Startbouwgepland": {
                    "gte": f"{year}-01-01",
                    "lte": f"{year}-12-31",
                    "format": "yyyy-MM-dd"
                }
            }
        }
    }

    # Voer de zoekopdracht uit en krijg de resultaten
    result = es.search(index=index_name, body=body)
    return result['hits']['hits']
