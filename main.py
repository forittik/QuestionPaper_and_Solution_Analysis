import streamlit as st
import pathlib
import os  # Import os module
from utils.pdf_to_image import pdf_page_to_jpeg
from utils.image_processing import process_image
from utils.api_helpers import configure_google_api, configure_openai_api
from utils.data_helpers import generate_student_responses, compare_answers, extract_solution_list

def main():
    st.title("JEE Exam Preparation - Question and Solution Processing")
    
    # Input PDFs for question paper and solutions
    question_pdf = st.file_uploader("Upload Question Paper PDF", type="pdf")
    solution_pdf = st.file_uploader("Upload Solution PDF", type="pdf")
    
    if question_pdf and solution_pdf:
        # Define the directory for saving PDFs
        pdf_directory = "data/PDFs/"

        # Check if the directory exists, if not, create it
        if not os.path.exists(pdf_directory):
            os.makedirs(pdf_directory, exist_ok=True)  # Avoid FileExistsError

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

        # Process images
        configure_google_api(st.text_input("Google API Key"))
        configure_openai_api(st.text_input("OpenAI API Key"))
        
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
