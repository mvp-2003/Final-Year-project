import os
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline
import time

root_dir = Path(__file__).resolve().parent.parent

if not torch.cuda.is_available():
    raise RuntimeError("GPU is not available. Please run this application on a machine with a GPU.")

pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1-base",
    torch_dtype=torch.float16
)

pipe.to("cuda")

def generate_sd_prompt(details):
    if not details:
        return None

    base_prompt = "Create a realistic portrait photograph of a person with these features:"
    feature_descriptions = []

    if 'gender' in details:
        gender = details['gender'].lower()
        feature_descriptions.append(f"a {gender} person")

    if 'hair color' in details:
        hair_color = details['hair color']
        feature_descriptions.append(f"with {hair_color} hair")

    if 'face shape' in details:
        face_shape = details['face shape'].lower()
        feature_descriptions.append(f"having a {face_shape} face shape")

    if 'has moustache' in details:
        has_moustache = details['has moustache'].lower() == 'yes'
        if has_moustache:
            feature_descriptions.append("with a well-groomed moustache")
        else:
            feature_descriptions.append("clean-shaven, without a moustache")

    features_text = ", ".join(feature_descriptions)
    detailed_prompt = f"{base_prompt} {features_text}. The image should be a professional headshot with a neutral background, good lighting, and sharp focus on facial features. Style: photorealistic portrait photography."

    return detailed_prompt

def generate_image(details):
    prompt = generate_sd_prompt(details)

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

        timestamp = int(time.time())
        image_filename = f"stable-diffusion-output-{timestamp}.png"
        image.save(image_filename)
        return image_filename
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None