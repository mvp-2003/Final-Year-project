import os
from dotenv import load_dotenv
from pathlib import Path
import requests

root_dir = Path(__file__).resolve().parent.parent
env_path = root_dir / '.env'

load_dotenv(dotenv_path=env_path)

def generate_dalle_prompt(details):
    if not details:
        return None

    base_prompt = "Create a realistic portrait photograph of a person with these features:"
    feature_descriptions = []

    if 'gender' in details:
        gender = details['gender'].lower()
        feature_descriptions.append(f"a {gender} person")

    if 'hair color' in details:
        hair_color = details['hair color']
        feature_descriptions.append(f"{hair_color} colored hair")

    if 'face shape' in details:
        face_shape = details['face shape'].lower()
        feature_descriptions.append(f"a {face_shape} face shape")

    if 'has moustache' in details:
        has_moustache = details['has moustache'].lower() == 'yes'
        if has_moustache:
            feature_descriptions.append("with a well-groomed moustache")
        else:
            feature_descriptions.append("clean-shaven, without a moustache")

    features_text = ", ".join(feature_descriptions)
    detailed_prompt = f"{base_prompt} {features_text}. The image should be a professional headshot with neutral background, good lighting, and sharp focus on facial features. Style: photorealistic portrait photography."

    return detailed_prompt

def generate_image(details):
    prompt = generate_dalle_prompt(details)

    if not prompt:
        return None

    try:
        response = requests.post(
            "https://api.flux.ai/v1/generate",
            json={
                "prompt": prompt,
                "size": "1024x1024",
                "n": 1,
            },
            headers={
                "Authorization": f"Bearer {os.getenv('FLUX_API_KEY')}",
                "Content-Type": "application/json"
            }
        )
        
        response.raise_for_status()
        return response.json()['data'][0]['url']
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None