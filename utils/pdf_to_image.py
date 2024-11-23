from pdf2image import convert_from_path
from PIL import Image
import os

def pdf_to_jpeg(pdf_path, output_folder="output_images"):
    """Convert a PDF file to JPEG images."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    images = convert_from_path(pdf_path, dpi=300)  # Adjust DPI for quality
    image_paths = []
    
    for i, image in enumerate(images):
        output_path = os.path.join(output_folder, f"page_{i + 1}.jpeg")
        image.save(output_path, "JPEG")
        image_paths.append(output_path)
    
    return image_paths
