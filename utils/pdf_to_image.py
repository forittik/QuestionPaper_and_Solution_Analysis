import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_jpeg(pdf_path, output_folder):
    """Convert PDF pages to JPEG images."""
    pdf_document = fitz.open(pdf_path)
    os.makedirs(output_folder, exist_ok=True)

    images = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Load page
        pix = page.get_pixmap()  # Render page to an image
        image_path = os.path.join(output_folder, f"page_{page_num + 1}.jpg")
        pix.save(image_path)  # Save as JPEG
        images.append(image_path)

    pdf_document.close()
    return images
