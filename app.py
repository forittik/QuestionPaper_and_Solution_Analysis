import streamlit as st
from utils.pdf_to_image import pdf_to_jpeg
from utils.image_processing import process_image
from utils.api_helpers import call_google_model, call_openai_model
from utils.data_helpers import compare_answers, generate_student_responses
import os
from frontend import *
st.title("Question Paper & Solution Analysis")

# File inputs for question paper and solution PDFs
question_pdf = st.file_uploader("Upload Question Paper PDF", type="pdf")
solution_pdf = st.file_uploader("Upload Solution PDF", type="pdf")

if question_pdf and solution_pdf:
    # Save PDFs locally
    question_pdf_path = f"data/question_paper.pdf"
    solution_pdf_path = f"data/solution.pdf"

    with open(question_pdf_path, "wb") as f:
        f.write(question_pdf.getbuffer())
    with open(solution_pdf_path, "wb") as f:
        f.write(solution_pdf.getbuffer())

    # Convert PDFs to images
    st.write("Converting PDFs to images...")
    question_images = pdf_to_jpeg(question_pdf_path, "data/question_images")
    solution_images = pdf_to_jpeg(solution_pdf_path, "data/solution_images")

    st.write("Processing images...")
    processed_data = []
    for img_path in question_images:
        result = process_image(img_path, api="google")
        processed_data.append(result)

    # Generate and compare answers
    st.write("Generating and comparing answers...")
    student_responses = generate_student_responses(processed_data)
    st.json(student_responses)

    # Save processed data to GitHub
    os.system("git add data && git commit -m 'Updated data' && git push origin main")
    st.success("Data saved to GitHub!")
