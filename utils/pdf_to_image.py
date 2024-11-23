import os
from pdf2image import convert_from_path
from PIL import Image

def pdf_page_to_jpeg(pdf_path, output_dir, page_numbers):
    """
    Convert specific pages of a PDF to JPEG images.

    Args:
    - pdf_path: Path to the input PDF file.
    - output_dir: Directory where JPEG files will be saved.
    - page_numbers: List of page numbers to be converted (1-indexed).

    Returns:
    - List of file paths for the generated JPEG images.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not isinstance(page_numbers, list) or not all(isinstance(num, int) for num in page_numbers):
        raise ValueError("page_numbers must be a list of integers (1-indexed).")

    os.makedirs(output_dir, exist_ok=True)

    # Convert the entire PDF to images
    images = convert_from_path(pdf_path, dpi=200)

    # Save specified pages to JPEG
    generated_images = []
    for page_num in page_numbers:
        if page_num < 1 or page_num > len(images):
            print(f"Page {page_num} is out of range.")
            continue

        image = images[page_num - 1]  # Convert from 1-indexed to 0-indexed
        output_path = os.path.join(output_dir, f"page_{page_num}.jpeg")
        image.save(output_path, "JPEG")
        generated_images.append(output_path)

    return generated_images
