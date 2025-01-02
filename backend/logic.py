def generate_response(extracted_details, user_message):
    questions = []
    
    if not extracted_details:
        questions.extend([
            "What's the gender of the suspect?",
            "What is the hair color?",
            "What is the face shape?",
            "Does the suspect have a moustache?"
        ])
    else:
        if 'gender' not in extracted_details:
            questions.append("What's the gender of the suspect?")
        if 'hair color' not in extracted_details:
            questions.append("What is the hair color?")
        if 'face shape' not in extracted_details:
            questions.append("What is the face shape?")
        if 'has moustache' not in extracted_details:
            questions.append("Does the suspect have a moustache?")

    if questions:
        response = "I need some more information:\n" + "\n".join(questions)
    else:
        gender_pronoun = "they"
        if 'gender' in extracted_details:
            if extracted_details['gender'].lower() in ['male', 'man']:
                gender_pronoun = "he"
            elif extracted_details['gender'].lower() in ['female', 'woman']:
                gender_pronoun = "she"

        details_list = []
        if 'hair color' in extracted_details:
            details_list.append(f"hair color is {extracted_details['hair color']}")
        if 'face shape' in extracted_details:
            details_list.append(f"face shape is {extracted_details['face shape']}")
        if 'moustache' in extracted_details:
            has_moustache = "has a moustache" if extracted_details['has moustache'].lower() == 'yes' else "doesn't have a moustache"
            details_list.append(has_moustache)

        response = f"Got it! The suspect's {', '.join(details_list)}. "
        if gender_pronoun != "they":
            response += f"And {gender_pronoun} is {extracted_details['gender']}."

    return response