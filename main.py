import os
import streamlit as st
import pathlib
from utils.pdf_to_image import pdf_page_to_jpeg
from utils.image_processing import process_image
from utils.api_helpers import configure_google_api, configure_openai_api
from utils.data_helpers import generate_student_responses, compare_answers, extract_solution_list
import genai  # Ensure genai module is imported for the GenerativeModel

def main():
    st.title("JEE Exam Preparation - Question and Solution Processing")
    
    # Input PDFs for question paper and solutions
    question_pdf = st.file_uploader("Upload Question Paper PDF", type="pdf")
    solution_pdf = st.file_uploader("Upload Solution PDF", type="pdf")
    
    if question_pdf and solution_pdf:
        # Define the directory for saving PDFs
        pdf_directory = "data/PDFs/"

        # Check if 'PDFs' is a file, and if so, remove it
        if os.path.exists(pdf_directory):
            if os.path.isfile(pdf_directory):
                os.remove(pdf_directory)  # Remove the file if it's a file, not a directory
            elif not os.path.isdir(pdf_directory):
                # In case it's neither a file nor a directory, handle the error
                st.error(f"Unexpected path: {pdf_directory} exists but is neither a file nor a directory.")
                return
        # Create the directory if it doesn't exist
        os.makedirs(pdf_directory, exist_ok=True)

        # Define file paths for saving uploaded PDFs
        question_pdf_path = f"{pdf_directory}{question_pdf.name}"
        solution_pdf_path = f"{pdf_directory}{solution_pdf.name}"

        # Save the PDFs to the specified directory
        with open(question_pdf_path, "wb") as f:
            f.write(question_pdf.read())
        
        with open(solution_pdf_path, "wb") as f:
            f.write(solution_pdf.read())
        
        # Convert PDF pages to images
        output_dir_questions = "data/output/question_images"
        output_dir_solutions = "data/output/solution_images"
        
        pdf_page_to_jpeg(question_pdf_path, output_dir_questions, [0, 1, 2])  # Example pages
        pdf_page_to_jpeg(solution_pdf_path, output_dir_solutions, [0, 1, 2])

        # Use API keys from Streamlit secrets
        google_api_key = st.secrets["google_api"]["api_key"]  # Replace with correct key from secrets.toml
        openai_api_key = st.secrets["openai_api"]["api_key"]  # Replace with correct key from secrets.toml
        
        # Configure APIs using the keys from secrets
        configure_google_api(google_api_key)
        configure_openai_api(openai_api_key)
        
        # Initialize the generative model
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        output_text = ""
        for image_path in pathlib.Path(output_dir_questions).glob("*.jpeg"):
            output_text += process_image(image_path, model, "Extract topics and concepts")

        st.subheader("Generated Topics and Concepts")
        st.write(output_text)
        
        # Further analysis for solutions
        solution_text = ""
        for image_path in pathlib.Path(output_dir_solutions).glob("*.jpeg"):
            solution_text += process_image(image_path, model, "Extract answers from the image")

        st.subheader("Extracted Solutions")
        st.write(solution_text)

        # You can further implement data processing, comparisons, etc., here

if __name__ == "__main__":
    main()
