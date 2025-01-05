import os
from dotenv import load_dotenv
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline

root_dir = Path(__file__).resolve().parent.parent
env_path = root_dir / '.env'

load_dotenv(dotenv_path=env_path)

hf_token = os.getenv('HUGGINGFACE_TOKEN')
if not hf_token:
    raise ValueError("HUGGINGFACE_TOKEN is not set in the environment variables.")

pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16,
    use_auth_token=hf_token
)

pipe.to("cpu")

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
        image = pipe(
            prompt,
            height=512,
            width=512,
            guidance_scale=7.5,
            num_inference_steps=50,
            generator=torch.Generator("cpu").manual_seed(0)
        ).images[0]

        image.save("stable-diffusion-output.png")
        return "stable-diffusion-output.png"
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None