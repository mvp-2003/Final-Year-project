from openai import AzureOpenAI
import os

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),  
    api_version="2024-02-15-preview",    # Check for latest API version
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")   # Your Azure OpenAI endpoint
)

def generate_dalle_prompt(details):
    """
    Generate a detailed prompt for DALL-E based on extracted features
    """
    if not details:
        return None

    # Base prompt template
    base_prompt = "Create a realistic portrait photograph of a person with these features:"

    # Feature descriptions
    feature_descriptions = []
    
    # Gender description
    if 'gender' in details:
        gender = details['gender'].lower()
        feature_descriptions.append(f"a {gender} person")
    
    # Hair description
    if 'hair color' in details:
        hair_color = details['hair color']
        feature_descriptions.append(f"{hair_color} colored hair")
    
    # Face shape description
    if 'face shape' in details:
        face_mappings = {
            'round': 'a round, soft face shape',
            'oval': 'an oval-shaped face with balanced proportions',
            'square': 'a strong, square-shaped face with defined jawline',
            'heart': 'a heart-shaped face with wider forehead and pointed chin',
            'rectangular': 'a rectangular face with elongated features',
            'diamond': 'a diamond-shaped face with defined cheekbones',
            'triangular': 'a triangular face shape with narrow forehead and wider jaw'
        }
        face_desc = face_mappings.get(details['face shape'].lower(), f"{details['face shape']} face shape")
        feature_descriptions.append(face_desc)
    
    # Moustache description
    if 'has moustache' in details:
        has_moustache = details['has moustache'].lower() == 'yes'
        if has_moustache:
            feature_descriptions.append("with a well-groomed moustache")
        else:
            feature_descriptions.append("clean-shaven, without a moustache")

    # Combine all features into a detailed prompt
    features_text = ", ".join(feature_descriptions)
    detailed_prompt = f"{base_prompt} {features_text}. The image should be a professional headshot with neutral background, good lighting, and sharp focus on facial features. Style: photorealistic portrait photography."

    return detailed_prompt

def generate_image(details):
    """
    Generate an image using DALL-E based on the extracted features
    """
    prompt = generate_dalle_prompt(details)
    
    if not prompt:
        return None
    
    try:
        response = client.images.generate(
            model="dall-e-3",  # Make sure this matches your deployed model name
            prompt=prompt,
            size="1024x1024",
            n=1,
        )
        
        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None