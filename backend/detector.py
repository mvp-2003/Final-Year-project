from transformers import pipeline

ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

def extract_details(message):
    entities = ner_pipeline(message)
    details = {}

    for entity in entities:
        if entity['entity_group'] in ['PER', 'ORG', 'LOC', 'MISC']:
            details[entity['entity_group']] = entity['word']
    
    return details
