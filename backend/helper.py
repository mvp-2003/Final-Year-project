required_details = ['gender', 'age', 'hair color', 'eye shape', 'eye color', 'facial structure', 'facial hair', 'nose shape']

def rephrase_details(details):
    rephrased = []
    for key, value in details.items():
        rephrased.append(f"{key} is {value}")
    return ". ".join(rephrased) + "."

def generate_image_with_dalle(details):
    # Call DALL-E API to generate an image
    # For simplicity, return a placeholder URL
    return "http://image.url"