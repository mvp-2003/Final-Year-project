from transformers import AutoModelForCausalLM, AutoTokenizer
from random import choice

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

initial_prompts = [
    ". I'm here to help identify suspects. What information can you share?",
    ". I'm ready to assist with suspect identification. What details do you have?",
    ". I'm here to help with the investigation. What can you tell me about the suspect?",
]

def initialize_chat_session():
    return {
        'details': {},
        'dialog_history': [],
        'context': "You are someonw who knows everything, perhaps the user's best friend. Keep chatting normally as here you will be working as a forensic artist and help the user to discuss about the suspect."
    }

def generate_dialog_response(input_text):
    input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt')
    chat_response_ids = model.generate(
        input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.9,
        top_p=0.95,
        no_repeat_ngram_size=3
    )
    return tokenizer.decode(chat_response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

def get_detail_context(current_details):
    detail_context = []
    if current_details:
        if 'gender' in current_details:
            detail_context.append(f"The suspect is {current_details['gender']}")
        if 'hair color' in current_details:
            detail_context.append(f"has {current_details['hair color']} hair")
        if 'face shape' in current_details:
            detail_context.append(f"has a {current_details['face shape']} face")
        if 'has moustache' in current_details:
            has_moustache = "has" if current_details['has moustache'].lower() == 'yes' else "doesn't have"
            detail_context.append(f"{has_moustache} a moustache")
    return detail_context

def process_chat(user_message, session_data):
    dialog_history = session_data['dialog_history']
    context = session_data['context']
    
    if not dialog_history:
        input_text = context + " " + user_message
    else:
        dialog_history.append(user_message)
        recent_messages = dialog_history[-3:] if len(dialog_history) > 3 else dialog_history
        input_text = context + " " + " ".join(recent_messages)
    
    dialog_response = generate_dialog_response(input_text)
    
    if not dialog_history and (not dialog_response or len(dialog_response.strip()) < 10):
        dialog_response = "Hello! Nice to meet you" + choice(initial_prompts)
    
    return dialog_response 