import os
import fitz
from PIL import Image

def pdf_page_to_jpeg(pdf_path, output_dir, page_numbers):
    """
    Convert specific pages of a PDF to JPEG images.

    Args:
    - pdf_path: Path to the input PDF file.
    - output_dir: Directory where JPEG files will be saved.
    - page_numbers: List of page numbers to be converted (0-indexed).
    """
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert each specified page to JPEG
    for page_num in page_numbers:
        # Ensure page number is valid
        if page_num < 0 or page_num >= len(pdf_document):
            print(f"Page {page_num + 1} is out of range.")
            continue

        # Load the page
        page = pdf_document.load_page(page_num)

        # Render the page to a pixmap (image representation in PyMuPDF)
        pix = page.get_pixmap()

        # Create a PIL Image from the pixmap's raw data
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Save the image as a JPEG file
        jpeg_filename = os.path.join(output_dir, f"page_{page_num + 1}.jpeg")
        image.save(jpeg_filename, "JPEG")

    # Close the PDF document
    pdf_document.close()
