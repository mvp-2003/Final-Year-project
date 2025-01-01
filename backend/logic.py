def generate_response(extracted_details, user_message):
    questions = []

    if 'gender' not in extracted_details:
        questions.append("What's the gender of the suspect?")
    if 'hair color' not in extracted_details:
        questions.append("What is the hair color?")
    if 'face shape' not in extracted_details:
        questions.append("What is the face shape?")
    if 'has moustache' not in extracted_details:
        questions.append("Does the suspect have a moustache?")

    if questions:
        response = " ".join(questions)
    else:
        gender_pronoun = "they"
        if 'gender' in extracted_details:
            if extracted_details['gender'].lower() in ['male', 'man']:
                gender_pronoun = "he"
            elif extracted_details['gender'].lower() in ['female', 'woman']:
                gender_pronoun = "she"

        response = f"Got it! The suspect's hair color is {extracted_details.get('hair color', 'unknown')}, " \
                   f"face shape is {extracted_details.get('face shape', 'unknown')}, and " \
                   f"the suspect is {gender_pronoun}."

    return response