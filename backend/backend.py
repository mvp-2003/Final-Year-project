from detector import extract_details
from logic import generate_response
from context import initialize_chat_session, process_chat, get_detail_context
from generator import generate_image

chat_history = {}

def process_chat_message(user_message, session_id='default'):
    """
    Process a chat message and return the appropriate response
    """
    if session_id not in chat_history:
        chat_history[session_id] = initialize_chat_session()
    
    # Extract and update details
    new_details = extract_details(user_message)
    current_details = chat_history[session_id]['details']
    current_details.update(new_details)
    chat_history[session_id]['details'] = current_details
    
    # Generate responses
    dialog_response = process_chat(user_message, chat_history[session_id])
    structured_response = generate_response(current_details, user_message)
    
    image_url = generate_image(current_details)  # Generate image based on details
    response = _format_response(dialog_response, structured_response, image_url)
    
    # Update chat history
    chat_history[session_id]['dialog_history'].append(response)
    
    # Update context
    _update_context(session_id, current_details)
    
    return response

def _format_response(dialog_response, structured_response, image_url):
    """
    Format the combined response from dialog and structured responses
    """
    if "I need some more information" in structured_response:
        if dialog_response and len(dialog_response.strip()) >= 10:
            return {
                'text': f"{dialog_response}\n\nBy the way, {structured_response.lower()}",
                'image_url': None
            }
        return {'text': structured_response, 'image_url': None}
    else:
        if dialog_response and len(dialog_response.strip()) >= 10:
            return {
                'text': f"{dialog_response}\n\nAlso, {structured_response}",
                'image_url': image_url
            }
        return {'text': structured_response, 'image_url': image_url}

def _update_context(session_id, current_details):
    """
    Update the context in chat history based on current details
    """
    detail_context = get_detail_context(current_details)
    if detail_context:
        chat_history[session_id]['context'] += " " + ", ".join(detail_context) + "." 