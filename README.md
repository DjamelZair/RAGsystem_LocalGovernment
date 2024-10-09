# RAG Permit System - Nieuwbouwplannen in Amsterdam

Dit project ontwikkelt een Retrieval-Augmented Generation (RAG) systeem waarmee vragen over nieuwbouwprojecten in Amsterdam beantwoord kunnen worden. Het systeem maakt gebruik van Elasticsearch voor zoeken en een Roberta-gebaseerde LLM (Language Model) voor extractieve vraag-en-antwoord verwerking.
De data gebruikt is publiekelijk toegankelijk: https://data.amsterdam.nl/data/datasets/
## Project Overzicht

Het project is opgezet in verschillende stappen:

1. **Data Preprocessing**: Het verwerken en opschonen van de data van nieuwbouwprojecten in Amsterdam.
2. **Elasticsearch**: Het opzetten van een Elasticsearch-index voor het opslaan en zoeken van de bouwprojectgegevens.
3. **Question Answering Pipeline**: Het gebruik van het Roberta-base model voor extractieve vraag-en-antwoord verwerking.
4. **Datumgebaseerde Zoekopdrachten**: Ondersteuning voor queries die jaartallen bevatten, zodat vragen zoals "Welke projecten starten in 2029?" correct worden beantwoord.

## Vereisten

- Python 3.9 of hoger
- Installaties via `pip`:

pip install pandas numpy elasticsearch transformers sentence-transformers

## Projectstructuur

- **data_preprocessing.py**: Verantwoordelijk voor het opschonen en voorbereiden van de data.
- **create_elasticsearch_index.py**: Zet de Elasticsearch-index op voor het opslaan van de bouwprojectgegevens.
- **elasticsearch_search.py**: Bevat zoekfuncties voor zowel tekstuele queries als datumgebaseerde queries.
- **rag_system.py**: Behandelt de vraagverwerking met behulp van de Roberta pipeline en Elasticsearch-resultaten.

## Installatie

1. Clone de repository:

    ```bash
    git clone https://github.com/jouw-gebruikersnaam/permit-system.git
    cd permit-system
    ```

2. Installeer de vereisten:

    ```bash
    pip install -r requirements.txt
    ```

3. Zorg ervoor dat Elasticsearch correct is geïnstalleerd en draait op je machine.

## Gebruik

### 1. Indexeer de data in Elasticsearch:
Voer eerst het script `create_elasticsearch_index.py` uit om de Elasticsearch-index op te zetten en de gegevens te indexeren:

   ```bash
   python create_elasticsearch_index.py
  ```

### 2. Stel je vragen over bouwprojecten:
Start het RAG-systeem door `rag_system.py` te runnen. Je kunt vragen stellen zoals:

```bash
python rag_system.py
```
### Voorbeeldvragen:

- "Welke bouwprojecten starten in 2029?"
- "Welke projecten worden er gebouwd in stadsdeel Noord?"

### Toekomstige Uitbreidingen

- Verbetering van de zoekfunctionaliteit met fuzzy matching.
- API-integratie voor real-time updates van de bouwprojecten.
- UI-ondersteuning voor gebruik zonder technische kennis.

### Uitdagingen

- **Keuze van het juiste LLM-model**: Experimenten met verschillende modellen zoals GPT2 en Roberta.
- **Inconsistente data**: Het opschonen van problematische waarden zoals `n.b.` in de dataset.
- **Datumgebaseerde zoekopdrachten**: Het correct afhandelen van zoekopdrachten die jaartallen bevatten in plaats van alleen tekstuele zoekvragen.

### Licentie

Dit project is gelicenseerd onder de MIT-licentie. Zie het LICENSE-bestand voor details.
