from PIL import Image
import numpy as np
from utils.api_helpers import call_google_model

def process_image(image_path, api="google"):
    """Process an image using the generative AI model."""
    image = Image.open(image_path)
    image_array = np.array(image)

    if api == "google":
        response = call_google_model(image_array)
    else:
        raise ValueError("Unsupported API.")
    return response
