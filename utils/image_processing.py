import PIL.Image
import google.generativeai as genai

def process_image(image_path, model, prompt):
    """
    Process a single image with the generative AI model.

    Args:
    - image_path: Path to the image file.
    - model: The generative AI model to process the image.
    - prompt: The prompt for the model.
    
    Returns:
    - The processed content from the model.
    """
    img = PIL.Image.open(image_path)

    # Call the model to generate content
    response = model.generate_content([prompt, img])

    # Return the response text for later use
    return response.text
