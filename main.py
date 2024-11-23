import os
import sys
import streamlit as st
import pathlib
from PIL import Image
import google.generativeai as genai
from tempfile import TemporaryDirectory
import subprocess
import platform

def install_dependencies():
    """Install required packages if they're missing."""
    try:
        import pdf2image
    except ImportError:
        st.warning("Installing required packages... Please wait.")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pdf2image", "Pillow"])
        st.success("Packages installed successfully! Please restart the application.")
        st.stop()

def check_poppler():
    """Check if poppler is installed and available in PATH."""
    try:
        from pdf2image import pdfinfo_from_path
        return True
    except Exception:
        os_name = platform.system().lower()
        if os_name == "linux":
            st.error("Poppler is missing. Install it using: `sudo apt-get install poppler-utils`")
        elif os_name == "darwin":
            st.error("Poppler is missing. Install it using: `brew install poppler`")
        else:
            st.error("Download Poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases/ and add it to PATH.")
        st.stop()
        return False

def configure_google_api(api_key):
    """Configure Google API with the provided key."""
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring Google API: {str(e)}")
        return False

def configure_openai_api(api_key):
    """Configure OpenAI API with the provided key."""
    try:
        os.environ["OPENAI_API_KEY"] = api_key
        return True
    except Exception as e:
        st.error(f"Error configuring OpenAI API: {str(e)}")
        return False

def pdf_to_jpeg(pdf_path, output_dir):
    """Convert PDF pages to JPEG images."""
    from pdf2image import convert_from_path  # Import after installation check
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=200)
        
        # Save each image
        for i, image in enumerate(images):
            image_path = os.path.join(output_dir, f"page_{i + 1}.jpeg")
            image.save(image_path, "JPEG")
        
        return True
    except Exception as e:
        st.error(f"Error converting PDF to images: {str(e)}")
        return False

def process_image(image_path, model, prompt):
    """Process an image using Google's Generative AI model."""
    try:
        with Image.open(image_path) as image:
            response = model.generate_content([prompt, image])
            return response.text + "\n\n"
    except Exception as e:
        st.error(f"Error processing image {image_path}: {str(e)}")
        return ""

def main():
    st.set_page_config(
        page_title="JEE Exam Analysis",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 JEE Exam Preparation - Question and Solution Processing")
    
    # Check and install dependencies
    install_dependencies()
    if not check_poppler():
        return
    
    # Add CSS for better file upload styling
    st.markdown("""
        <style>
        .stFileUploader > div > div {
            padding: 20px;
            border: 2px dashed #ccc;
            border-radius: 6px;
        }
        .stAlert > div {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # API key configuration section
    with st.sidebar:
        st.header("API Configuration")
        use_secrets = st.checkbox("Use secrets.toml configuration", value=True)
        
        if use_secrets:
            try:
                google_api_key = st.secrets["google_api"]["api_key"]
                openai_api_key = st.secrets["openai_api"]["api_key"]
            except Exception:
                st.error("secrets.toml file not found or missing API keys.")
                st.stop()
        else:
            google_api_key = st.text_input("Enter Google API Key", type="password")
            openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
            
            if not google_api_key or not openai_api_key:
                st.warning("Please enter both API keys to continue.")
                st.stop()
    
    # Main content
    st.write("### Upload Your Files")
    st.write("Please upload your question paper and solution PDFs below:")
    
    col1, col2 = st.columns(2)
    with col1:
        question_pdf = st.file_uploader("Upload Question Paper PDF", type="pdf")
    
    with col2:
        solution_pdf = st.file_uploader("Upload Solution PDF", type="pdf")
    
    if question_pdf and solution_pdf:
        with st.spinner("Processing your PDFs... This may take a few moments."):
            # Create temporary directory for processing
            with TemporaryDirectory() as temp_dir:
                question_pdf_path = os.path.join(temp_dir, "question.pdf")
                solution_pdf_path = os.path.join(temp_dir, "solution.pdf")
                
                # Save uploaded files
                with open(question_pdf_path, "wb") as f:
                    f.write(question_pdf.getvalue())
                with open(solution_pdf_path, "wb") as f:
                    f.write(solution_pdf.getvalue())
                
                # Convert PDFs to images
                output_dir_questions = os.path.join(temp_dir, "question_images")
                output_dir_solutions = os.path.join(temp_dir, "solution_images")
                
                if not pdf_to_jpeg(question_pdf_path, output_dir_questions):
                    st.error("Failed to process question paper PDF.")
                    st.stop()
                
                if not pdf_to_jpeg(solution_pdf_path, output_dir_solutions):
                    st.error("Failed to process solution PDF.")
                    st.stop()
                
                # Configure APIs
                if not (configure_google_api(google_api_key) and configure_openai_api(openai_api_key)):
                    st.error("Failed to configure APIs. Please check your API keys.")
                    st.stop()
                
                # Initialize the generative model
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                
                # Process question paper
                st.write("### Analysis Results")
                with st.expander("Question Paper Analysis", expanded=True):
                    output_text = ""
                    for image_path in sorted(pathlib.Path(output_dir_questions).glob("*.jpeg")):
                        output_text += process_image(image_path, model, "Extract topics and concepts from this question.")
                    st.write(output_text if output_text else "No content extracted.")
                
                # Process solutions
                with st.expander("Solution Analysis", expanded=True):
                    solution_text = ""
                    for image_path in sorted(pathlib.Path(output_dir_solutions).glob("*.jpeg")):
                        solution_text += process_image(image_path, model, "Extract solutions and explanations.")
                    st.write(solution_text if solution_text else "No content extracted.")

if __name__ == "__main__":
    main()
