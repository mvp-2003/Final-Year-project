from transformers import pipeline
import re

chat_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")

def extract_details(message):
    details = {}

    patterns = {
        'gender': r'\b(?:gender\s*is\s*)?(male|female|other)\b',
        'age': r'\b(?:age\s*is\s*)?(\d{1,2})\b',
        'hair color': r'\b(?:hair\s*color\s*is\s*|hair\s*is\s*)(black|brown|blonde|red|grey|white|green)\b',
        'eye color': r'\b(?:eye\s*color\s*is\s*|eyes\s*are\s*|eyes\s*were\s*)(blue|green|brown|hazel|grey)\b',
        'facial structure': r'\b(?:facial\s*structure\s*is\s*)?(round|oval|square|heart)\b',
        'facial hair': r'\b(?:facial\s*hair\s*is\s*)?(beard|mustache|clean-shaven|clean shaved|no facial hairs)\b',
        'nose shape': r'\b(?:nose\s*shape\s*is\s*)?(straight|hooked|button|upturned)\b'
    }

    for detail, pattern in patterns.items():
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            details[detail] = match.group(1)

    return details

def generate_conversational_response(user_message):
    conversation = chat_pipeline(user_message)
    return conversation.generated_responses[0]
