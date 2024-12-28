def generate_response(extracted_details, user_message):
    if 'hair color' in extracted_details and 'eye color' in extracted_details:
        response = "Got it! Hair color is {} and eye color is {}.".format(
            extracted_details['hair color'], extracted_details['eye color']
        )
    elif 'color' in extracted_details:
        response = "I see you mentioned the color '{}'. Is this for hair or eyes?".format(
            extracted_details['color']
        )
    elif "how was your day" in user_message.lower():
        response = "I'm just a program, but I'm here to help you! How can I assist you today?"
    else:
        response = "Could you please provide more details about the features?"

    return response