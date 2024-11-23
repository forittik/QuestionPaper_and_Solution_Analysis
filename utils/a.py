import fitz
from PIL import Image
import os

def pdf_to_jpeg(pdf_path, output_dir, page_numbers):
    """
    Convert specific pages of a PDF to JPEG images.

    Args:
    - pdf_path: Path to the input PDF file.
    - output_dir: Directory where JPEG files will be saved.
    - page_numbers: List of page numbers to be converted (0-indexed).
    """
    pdf_document = fitz.open(pdf_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for page_num in page_numbers:
        if page_num < 0 or page_num >= len(pdf_document):
            continue

        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        jpeg_filename = os.path.join(output_dir, f"page_{page_num + 1}.jpeg")
        image.save(jpeg_filename, "JPEG")

    pdf_document.close()
