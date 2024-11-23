import google.generativeai as genai
import openai

# Call to Google AI model
def call_google_model(image):
    response = genai.GenerativeModel('gemini-1.5-pro-latest').generate_content([
        "Extract topics from the image", image
    ])
    return response.text

# Call to OpenAI model
def call_openai_model(student_data, solution_output, test_number):
    context = f"""
    You are an intelligent agent for JEE exam preparation. Provide a detailed SOCA report for each student.
    Paper: {solution_output}
    Answer state: {student_data}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": context}]
    )
    return response['choices'][0]['message']['content']
