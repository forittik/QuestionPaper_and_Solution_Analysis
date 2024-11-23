from pdf2image import convert_from_bytes
from PIL import Image
import os

def pdf_to_images(pdf_file):
    """Convert PDF to a list of images."""
    images = convert_from_bytes(pdf_file.read())
    image_paths = []
    for i, img in enumerate(images):
        path = f"data/page_{i + 1}.jpg"
        img.save(path, "JPEG")
        image_paths.append(path)
    return image_paths
