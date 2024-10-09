import pandas as pd
from elasticsearch import Elasticsearch

# ------------------------------
# Step 1: Load and Explore CSV Data
# ------------------------------

file_path = '/home/amadeo/Documents/permit_system/AmsterdamData/cleaned_nieuwbouwplannen.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Preprocess: Convert date fields to a consistent format
df['Startbouwgepland'] = pd.to_datetime(df['Startbouwgepland'], errors='coerce').dt.strftime('%Y-%m-%d')

# Nieuwe boolean kolom voor 'Startbouwgerealiseerd'
df['BouwGestart'] = df['Startbouwgerealiseerd'].notna()

# Vul 'NaN' voor tekstvelden met 'n.b.' en voor numerieke velden met 0
df.fillna({
    'Buurtcode': 'n.b.',
    'Buurtnaam': 'n.b.',
    'Wijkcode': 'n.b.',
    'Wijknaam': 'n.b.',
    'Gebiedcode': 'n.b.',
    'Gebiednaam': 'n.b.',
    'Stadsdeelcode': 'n.b.',
    'Stadsdeelnaam': 'n.b.',
    'Zelfbouw': 'n.b.',
    'Socialehuurcorporatie': 'n.b.',
    'Jongeren': 'n.b.',
    'Studenten': 'n.b.',
    'Shonzelfstenoftijdelijk': 'n.b.',
    'Onzelfstandig': 'n.b.',
    'Tijdelijk': 'n.b.',
    'Socialehuurzelfstperm': 0,
    'Middeldurehuur': 0,
    'Socialekoop': 0,
    'Vrijesectorhuur': 0,
    'Vrijesectorkoop': 0,
    'Vrijesectornb': 0,
    'Onbekend': 0,
    'Totaal': 0,
    'Totaalzelfstperm': 0
}, inplace=True)

# Verwijder het originele 'Startbouwgerealiseerd' veld
df = df.drop(columns=['Startbouwgerealiseerd'])

# ------------------------------
# Step 2: Define Mapping for ElasticSearch
# ------------------------------

# Initialize ElasticSearch connection
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Define the mapping for the index
mapping = {
    "mappings": {
        "properties": {
            "Id": {"type": "integer"},
            "Projectnaamafkorting": {"type": "text"},
            "Buurtcode": {"type": "keyword"},
            "Buurtnaam": {"type": "text"},
            "Wijkcode": {"type": "keyword"},
            "Wijknaam": {"type": "text"},
            "Gebiedcode": {"type": "keyword"},
            "Gebiednaam": {"type": "text"},
            "Stadsdeelcode": {"type": "keyword"},
            "Stadsdeelnaam": {"type": "text"},
            "Zelfbouw": {"type": "text"},
            "Socialehuurcorporatie": {"type": "text"},
            "Plaberumpublicatie": {"type": "text"},
            "Startbouwgepland": {"type": "date", "format": "yyyy-MM-dd"},
            "BouwGestart": {"type": "boolean"},  # Nieuw boolean veld voor bouwstatus
            "Socialehuurzelfstperm": {"type": "integer"},
            "Middeldurehuur": {"type": "integer"},
            "Socialekoop": {"type": "integer"},
            "Vrijesectorhuur": {"type": "integer"},
            "Vrijesectorkoop": {"type": "integer"},
            "Vrijesectornb": {"type": "integer"},
            "Onbekend": {"type": "integer"},
            "Jongeren": {"type": "text"},
            "Studenten": {"type": "text"},
            "Shonzelfstenoftijdelijk": {"type": "text"},
            "Onzelfstandig": {"type": "text"},
            "Tijdelijk": {"type": "text"},
            "Totaal": {"type": "integer"},
            "Totaalzelfstperm": {"type": "integer"},
            "Peildatum": {"type": "date", "format": "yyyy-MM-dd"}
        }
    }
}

# Create the index with the defined mapping
index_name = 'nieuwbouwplannen'
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)

# ------------------------------
# Step 3: Index Data into ElasticSearch
# ------------------------------

# Function to index data in ElasticSearch
def index_data(df, index_name='nieuwbouwplannen'):
    print(f"Indexing data into ElasticSearch with index '{index_name}'...")
    for idx, row in df.iterrows():
        doc = row.to_dict()
        
        # Remove any unnecessary fields
        doc.pop('Geometrie', None)
        
        try:
            # Index the document in ElasticSearch
            es.index(index=index_name, id=idx, body=doc)
        except Exception as e:
            print(f"Error indexing row {idx}: {e}")
            print(f"Problematic document: {doc}")
    
    print(f"Indexing completed for {len(df)} records.")

# Index the data
index_data(df)
