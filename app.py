import streamlit as st
from utils.pdf_to_image import pdf_to_images
from utils.image_processing import process_images
from utils.api_helpers import call_google_model, call_openai_model
from utils.data_helpers import compare_answers


# Title and description
st.title("Question Paper and Solution Analysis")
st.write("Upload question paper and solution PDFs to analyze and compare!")

# File upload
question_pdf = st.file_uploader("Upload Question Paper PDF", type=["pdf"])
solution_pdf = st.file_uploader("Upload Solution PDF", type=["pdf"])

if question_pdf and solution_pdf:
    # Convert PDFs to images
    st.write("Converting PDFs to images...")
    question_images = pdf_to_images(question_pdf)
    solution_images = pdf_to_images(solution_pdf)

    # Process images using AI models
    st.write("Processing images with AI models...")
    question_data = process_images(question_images)
    solution_data = process_images(solution_images)

    # Compare answers
    st.write("Comparing question paper with solutions...")
    result = compare_answers(question_data, solution_data)

    # Display results
    st.write("Analysis Complete!")
    st.json(result)  # Show results in JSON format

    # Save results to GitHub
    st.write("Saving results to GitHub...")
    from utils.api_helpers import save_to_github
    save_to_github("data/output.json", result)
    st.success("Results saved to GitHub!")
