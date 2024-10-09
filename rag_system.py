from transformers import pipeline
from elasticsearch_search import search_with_embeddings, search_by_date
import re  # Dit gebruiken we om te zoeken naar jaartallen in de vraag

# Laad Roberta model voor extractieve QA (Question Answering)
# Hier gebruiken we de Roberta-base model die is getraind op SQuAD2.0 data voor extractieve vraag-antwoord taken.
model_name = "deepset/roberta-base-squad2"
qa_pipeline = pipeline('question-answering', model=model_name, tokenizer=model_name)

# Functie om een antwoord te extraheren uit de gegeven context op basis van de vraag.
def extract_answer(question, context):
    # Bereid de input voor het QA-model voor met de vraag en de context
    qa_input = {
        'question': question,  # De vraag die we willen beantwoorden
        'context': context  # De context waarin we het antwoord verwachten te vinden
    }
    # Haal het antwoord op uit het model
    result = qa_pipeline(qa_input)['answer']
    
    # Controleer of het antwoord zinvol is. Als het antwoord generieke termen zoals "bouw", "aantal" of "onbekend" bevat,
    # geef dan "Niet beschikbaar" terug.
    if result.strip().lower() in ["bouw", "aantal", "onbekend"]:
        return "Niet beschikbaar"
    return result  # Retourneer anders het antwoord zoals het is.

# Functie om te bepalen of de vraag een jaartal bevat
def contains_year(question):
    # Zoekt naar een jaartal in de vraag (bijv. "2029" of "in 2029")
    match = re.search(r'\b(19|20)\d{2}\b', question)
    return match.group(0) if match else None

# Functie om een antwoord te genereren op basis van de vraag en zoekresultaten uit Elasticsearch
def generate_answer(question, index_name='nieuwbouwplannen'):
    # Controleer of de vraag een jaartal bevat
    year = contains_year(question)
    
    if year:
        # Als er een jaartal is gevonden, gebruik de datumgebaseerde zoekfunctie
        search_results = search_by_date(year, index_name)
    else:
        # Gebruik anders de tekstgebaseerde zoekfunctie
        search_results = search_with_embeddings(question, index_name)
    
    # Als er geen resultaten zijn, geven we een standaardboodschap terug
    if not search_results:
        return "Er zijn op dit moment geen bouwprojecten gevonden in het opgegeven gebied."
    
    # Stap 2: Bouw een overzicht van de gevonden projecten
    all_projects = []
    
    # We gaan door de eerste 3 zoekresultaten heen om het overzicht simpel te houden
    for hit in search_results[:3]:
        # Maak een contextstring die alle relevante informatie over het project bevat
        context = (f"Project: {hit['_source']['Projectnaamafkorting']}, "
                   f"Stadsdeel: {hit['_source']['Stadsdeelnaam']}, "
                   f"Status: {'Gestart' if hit['_source']['BouwGestart'] else 'Niet gestart'}, "
                   f"Aantal woningen: {hit['_source'].get('Totaal', 'Onbekend')}, "
                   f"Start bouw gepland op: {hit['_source']['Startbouwgepland']}")
        
        # Gebruik de extractieve QA om antwoorden te krijgen op drie vragen:
        # 1. Wat is de status van het project?
        # 2. Hoeveel woningen worden er gebouwd?
        # 3. Wanneer start de bouw?
        project_info = {
            "naam": hit['_source']['Projectnaamafkorting'],  # Naam van het project
            "status": extract_answer("Wat is de status van dit project?", context),  # Status
            "aantal_woningen": extract_answer("Hoeveel woningen worden er gebouwd?", context),  # Aantal woningen
            "start_bouw": extract_answer("Wanneer start de bouw?", context)  # Startdatum bouw
        }
        all_projects.append(project_info)  # Voeg de projectinformatie toe aan de lijst van alle projecten
    
    # Stap 3: Format het antwoord zodat het leesbaar is voor de gebruiker
    answer = "Hier zijn de relevante bouwprojecten:\n"
    for project in all_projects:
        answer += (f"Project: {project['naam']}\n"
                   f"Status: {project['status']}\n"
                   f"Aantal woningen: {project['aantal_woningen']}\n"
                   f"Start bouw: {project['start_bouw']}\n\n")
    
    return answer  # Retourneer het geformatteerde antwoord.

# Dit is de main-functie waarin de gebruiker een vraag kan stellen
if __name__ == "__main__":
    # Vraag de gebruiker om een vraag in te typen
    question = input("Stel je vraag over bouwprojecten: ")
    
    # Genereer het antwoord op basis van de vraag
    answer = generate_answer(question)
    
    # Print het antwoord naar de console
    print(f"Antwoord:\n{answer}")
