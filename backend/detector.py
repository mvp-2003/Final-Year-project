from transformers import pipeline

ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

def extract_details(message):
    entities = ner_pipeline(message)
    details = {}

    for entity in entities:
        if entity['entity_group'] == 'PER':
            details['gender'] = entity['word']
        elif entity['entity_group'] == 'AGE':
            details['age'] = entity['word']
        elif entity['entity_group'] == 'COLOR':
            if 'hair color' not in details:
                details['hair color'] = entity['word']
            else:
                details['eye color'] = entity['word']

    return details
