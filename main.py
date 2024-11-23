import os
import streamlit as st
import pathlib
from PIL import Image
import pdf2image  # Using pdf2image instead of PyMuPDF
import google.generativeai as genai
from tempfile import TemporaryDirectory

def configure_google_api(api_key):
    """Configure Google API with the provided key."""
    genai.configure(api_key=api_key)

def configure_openai_api(api_key):
    """Configure OpenAI API with the provided key."""
    os.environ["OPENAI_API_KEY"] = api_key

def pdf_to_jpeg(pdf_path, output_dir, page_numbers):
    """Convert PDF pages to JPEG images using pdf2image."""
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Convert PDF to images
        images = pdf2image.convert_from_path(
            pdf_path,
            dpi=200,
            first_page=min(page_numbers) + 1,
            last_page=max(page_numbers) + 1
        )
        
        # Save each image
        for i, image in enumerate(images):
            image_path = os.path.join(output_dir, f"page_{page_numbers[i]}.jpeg")
            image.save(image_path, "JPEG")
            
        return True
    except Exception as e:
        st.error(f"Error converting PDF to images: {str(e)}")
        return False

def process_image(image_path, model, prompt):
    """Process an image using Google's Generative AI model."""
    try:
        image = Image.open(image_path)
        response = model.generate_content([prompt, image])
        return response.text + "\n\n"
    except Exception as e:
        st.error(f"Error processing image {image_path}: {str(e)}")
        return ""

def main():
    st.title("JEE Exam Preparation - Question and Solution Processing")
    
    # Add CSS for better file upload styling
    st.markdown("""
        <style>
        .stFileUploader > div > div {
            padding: 20px;
            border: 2px dashed #ccc;
            border-radius: 6px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Input PDFs with clear instructions
    st.write("### Upload Your Files")
    st.write("Please upload your question paper and solution PDFs below:")
    
    question_pdf = st.file_uploader("Upload Question Paper PDF", type="pdf", help="Upload the JEE question paper in PDF format")
    solution_pdf = st.file_uploader("Upload Solution PDF", type="pdf", help="Upload the corresponding solutions in PDF format")
    
    if question_pdf and solution_pdf:
        with st.spinner("Processing your PDFs..."):
            # Create temporary directory for processing
            with TemporaryDirectory() as temp_dir:
                # Save uploaded PDFs to temporary directory
                question_pdf_path = os.path.join(temp_dir, "question.pdf")
                solution_pdf_path = os.path.join(temp_dir, "solution.pdf")
                
                with open(question_pdf_path, "wb") as f:
                    f.write(question_pdf.getvalue())
                with open(solution_pdf_path, "wb") as f:
                    f.write(solution_pdf.getvalue())
                
                # Create output directories
                output_dir_questions = os.path.join(temp_dir, "question_images")
                output_dir_solutions = os.path.join(temp_dir, "solution_images")
                
                # Convert PDFs to images
                if not pdf_to_jpeg(question_pdf_path, output_dir_questions, [0, 1, 2]):
                    st.error("Failed to process question paper PDF")
                    return
                
                if not pdf_to_jpeg(solution_pdf_path, output_dir_solutions, [0, 1, 2]):
                    st.error("Failed to process solution PDF")
                    return
                
                try:
                    # Configure APIs
                    google_api_key = st.secrets["google_api"]["api_key"]
                    openai_api_key = st.secrets["openai_api"]["api_key"]
                    
                    configure_google_api(google_api_key)
                    configure_openai_api(openai_api_key)
                    
                    # Initialize the generative model
                    model = genai.GenerativeModel('gemini-1.5-pro-latest')
                    
                    # Process question paper
                    st.write("### Analysis Results")
                    with st.expander("Question Paper Analysis", expanded=True):
                        output_text = ""
                        for image_path in pathlib.Path(output_dir_questions).glob("*.jpeg"):
                            output_text += process_image(image_path, model, "Extract topics and concepts")
                        st.write(output_text)
                    
                    # Process solutions
                    with st.expander("Solution Analysis", expanded=True):
                        solution_text = ""
                        for image_path in pathlib.Path(output_dir_solutions).glob("*.jpeg"):
                            solution_text += process_image(image_path, model, "Extract answers from the image")
                        st.write(solution_text)
                    
                except Exception as e:
                    st.error(f"An error occurred during processing: {str(e)}")
                    st.info("Please ensure your API keys are correctly configured in the secrets.toml file")

if __name__ == "__main__":
    main()
