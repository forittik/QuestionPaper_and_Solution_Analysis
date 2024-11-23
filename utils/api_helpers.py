import google.generativeai as genai
import openai

def configure_google_api(api_key):
    genai.configure(api_key=api_key)

def configure_openai_api(api_key):
    openai.api_key = api_key

def generate_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
