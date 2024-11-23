import streamlit as st
import os
import pathlib
from utils.pdf_to_image import pdf_to_jpeg
from utils.image_processing import process_image
from utils.api_helpers import call_google_model, call_openai_model
from utils.data_helpers import compare_answers, generate_student_responses
import google.generativeai as genai
import openai

# Ensure API keys are passed properly
def initialize_api_keys():
    # Set the API key for Google Generative AI
    google_api_key = st.secrets["google_api_key"]  # Store Google API key in Streamlit secrets
    genai.configure(api_key=google_api_key)
    
    # Set the API key for OpenAI
    openai.api_key = st.secrets["openai_api_key"]  # Store OpenAI API key in Streamlit secrets

# Function to convert the uploaded PDFs to images
def handle_pdf_upload(pdf_file, output_dir, page_numbers):
    pdf_path = os.path.join(output_dir, pdf_file.name)
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file.read())
    
    # Convert the uploaded PDF pages to images
    pdf_to_jpeg(pdf_path, output_dir, page_numbers)

# Main Streamlit app layout
def main():
    st.title("JEE Exam Paper Analysis and SOCA Generation")

    st.sidebar.header("User Input")

    # PDF file upload (question paper and solution)
    question_pdf = st.sidebar.file_uploader("Upload the Question Paper PDF", type=["pdf"])
    solution_pdf = st.sidebar.file_uploader("Upload the Solution PDF", type=["pdf"])

    if question_pdf and solution_pdf:
        st.sidebar.success("Both PDFs uploaded successfully!")

        page_numbers = st.sidebar.text_input("Enter page numbers to process (comma-separated)", "1,2,3").split(',')
        page_numbers = [int(p.strip()) - 1 for p in page_numbers]  # 0-indexed

        output_dir = 'data'  # Folder to store images and outputs

        # Process the question paper and solution PDFs
        question_image_dir = os.path.join(output_dir, 'question_images')
        solution_image_dir = os.path.join(output_dir, 'solution_images')

        # Ensure the directories exist
        pathlib.Path(question_image_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(solution_image_dir).mkdir(parents=True, exist_ok=True)

        # Convert both question paper and solution PDFs to images
        handle_pdf_upload(question_pdf, question_image_dir, page_numbers)
        handle_pdf_upload(solution_pdf, solution_image_dir, page_numbers)

        # Process images for question and solution papers
        question_images = sorted(pathlib.Path(question_image_dir).glob('*.jpeg'))
        solution_images = sorted(pathlib.Path(solution_image_dir).glob('*.jpeg'))

        # Display the images and their respective outputs
        st.header("Question Paper and Solution Analysis")

        # Process question images
        question_output = []
        for image_file in question_images:
            output = process_image(image_file, 'google')  # Call to the Google generative model
            question_output.append(output)
            st.image(image_file, caption=f"Question Paper - {image_file.name}", use_column_width=True)
            st.subheader(f"Output for {image_file.name}")
            st.markdown(output)

        # Process solution images
        solution_output = []
        for image_file in solution_images:
            output = process_image(image_file, 'openai')  # Call to the OpenAI model
            solution_output.append(output)
            st.image(image_file, caption=f"Solution Paper - {image_file.name}", use_column_width=True)
            st.subheader(f"Output for {image_file.name}")
            st.markdown(output)

        # Generate student responses
        student_answers = generate_student_responses(num_students=5)

        # Compare student answers with solution
        solution_list = [int(num) for num in solution_output[0].split()]
        comparison_results = compare_answers(solution_list, student_answers[0])

        st.header("Comparison of Student Answers")
        st.write(comparison_results)

        # Display SOCA analysis (using OpenAI for SOCA)
        test_number = 1
        student_data = {"student_1": student_answers[0]}  # For demo purposes, using first student's responses
        soca_analysis = call_openai_model(student_data, solution_output, test_number)
        st.subheader("SOCA Analysis")
        st.markdown(soca_analysis)

    else:
        st.warning("Please upload both the Question Paper and Solution PDFs to proceed.")

if __name__ == "__main__":
    initialize_api_keys()  # Initialize API keys here
    main()
