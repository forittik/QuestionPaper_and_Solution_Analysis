import PIL.Image
from utils.api_helpers import call_google_model, call_openai_model

def process_image(image_path, model_type):
    img = PIL.Image.open(image_path)

    if model_type == 'google':
        response = call_google_model(img)
    elif model_type == 'openai':
        response = call_openai_model(img)
    else:
        raise ValueError("Invalid model type")

    return response
