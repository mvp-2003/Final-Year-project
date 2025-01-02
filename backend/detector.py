from transformers import pipeline

ner_pipeline = pipeline("ner", model="dbmdz/bert-base-cased-finetuned-conll03-english", aggregation_strategy="simple")

def extract_details(message):
    entities = ner_pipeline(message)
    details = {}
    
    message_lower = message.lower()
    
    hair_colors = ['black', 'brown', 'blonde', 'red', 'grey', 'white', 'blue', 'green', 'purple']
    for color in hair_colors:
        if color in message_lower and 'hair' in message_lower:
            details['hair color'] = color
            break
    
    if 'male' in message_lower or 'man' in message_lower:
        details['gender'] = 'male'
    elif 'female' in message_lower or 'woman' in message_lower:
        details['gender'] = 'female'
    
    face_shapes = ['round', 'oval', 'square', 'heart', 'rectangular', 'diamond', 'triangular']
    for shape in face_shapes:
        if shape in message_lower and ('face' in message_lower or 'facial' in message_lower):
            details['face shape'] = shape
            break
    
    if 'moustache' in message_lower or 'mustache' in message_lower:
        if 'no' in message_lower or "doesn't" in message_lower or 'not' in message_lower:
            details['has moustache'] = 'no'
        else:
            details['has moustache'] = 'yes'

    for entity in entities:
        if entity['entity_group'] == 'PER' and 'gender' not in details:
            details['gender'] = entity['word']
        elif entity['entity_group'] == 'COLOR' and 'hair color' not in details:
            details['hair color'] = entity['word']
        elif entity['entity_group'] == 'SHAPE' and 'face shape' not in details:
            details['face shape'] = entity['word']

    return details
