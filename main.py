import os
import sys
import streamlit as st
import pathlib
from PIL import Image
import google.generativeai as genai
from tempfile import TemporaryDirectory
import subprocess
import platform
import shutil

def check_poppler_installation():
    """
    Check if poppler is installed and available in the system PATH.
    Returns tuple of (is_installed: bool, installation_instructions: str)
    """
    os_name = platform.system().lower()
    
    # Check if poppler-utils is in PATH
    poppler_path = shutil.which('pdftoppm') if os_name != 'windows' else shutil.which('pdftoppm.exe')
    
    if poppler_path:
        return True, ""
    
    # Prepare OS-specific installation instructions
    if os_name == "linux":
        instructions = """
        Poppler is not installed. Please install it using these commands:
        ```bash
        sudo apt-get update
        sudo apt-get install -y poppler-utils
        ```
        After installation, please restart your application.
        """
    elif os_name == "darwin":
        instructions = """
        Poppler is not installed. Please install it using Homebrew:
        ```bash
        brew install poppler
        ```
        After installation, please restart your application.
        """
    elif os_name == "windows":
        instructions = """
        Poppler is not installed. Please follow these steps:
        1. Download Poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases/
        2. Extract the downloaded file
        3. Add the extracted folder's 'bin' directory to your system PATH
        4. Restart your computer
        5. Restart this application
        """
    else:
        instructions = "Poppler installation not supported for your operating system."
    
    return False, instructions

def install_dependencies():
    """Install required Python packages if they're missing."""
    required_packages = ['pdf2image', 'Pillow']
    
    try:
        import pdf2image
        return True
    except ImportError:
        st.warning("Installing required packages... Please wait.")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + required_packages)
            st.success("Python packages installed successfully! Please restart the application.")
            st.stop()
            return False
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to install required packages: {str(e)}")
            st.stop()
            return False

def pdf_to_jpeg(pdf_path, output_dir):
    """Convert PDF pages to JPEG images with enhanced error handling."""
    from pdf2image import convert_from_path
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # First check if the PDF exists and is readable
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        # Get poppler path for Windows
        poppler_path = None
        if platform.system().lower() == "windows":
            # Try to find poppler in common installation locations
            possible_paths = [
                r"C:\Program Files\poppler-xx\bin",
                r"C:\Program Files (x86)\poppler-xx\bin",
                os.path.join(os.getenv('USERPROFILE', ''), 'poppler-xx\bin')
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    poppler_path = path
                    break
        
        # Convert PDF to images
        images = convert_from_path(
            pdf_path,
            dpi=200,
            poppler_path=poppler_path,
            thread_count=os.cpu_count() or 1
        )
        
        # Save each image
        for i, image in enumerate(images):
            image_path = os.path.join(output_dir, f"page_{i + 1}.jpeg")
            image.save(image_path, "JPEG", quality=85, optimize=True)
        
        return True
    except Exception as e:
        error_msg = str(e)
        if "poppler" in error_msg.lower():
            is_installed, instructions = check_poppler_installation()
            if not is_installed:
                st.error("Poppler Error: " + instructions)
            else:
                st.error(f"Error with Poppler: {error_msg}")
        else:
            st.error(f"Error converting PDF to images: {error_msg}")
        return False

def main():
    st.set_page_config(
        page_title="JEE Exam Analysis",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 JEE Exam Preparation - Question and Solution Processing")
    
    # Check dependencies first
    if not install_dependencies():
        return
        
    # Check Poppler installation with better error handling
    try:
        poppler_installed, install_instructions = check_poppler_installation()
        if not poppler_installed:
            st.error("Poppler is not installed or not found in PATH")
            st.markdown(install_instructions)
            
            # Add deployment-specific instructions
            st.markdown("""
            ### For Streamlit Cloud Deployment:
            If you're seeing this error on Streamlit Cloud:
            1. Make sure you have a `packages.txt` file in your repository root
            2. The file should contain: `poppler-utils`
            3. Redeploy your application
            """)
            st.stop()
            return
    except Exception as e:
        st.error(f"Error checking Poppler installation: {str(e)}")
        st.stop()
        return

    # API Configuration
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
    # Rest of your existing main() function code remains the same...
    # (Previous code for API configuration, file upload, and processing)

if __name__ == "__main__":
    main()
