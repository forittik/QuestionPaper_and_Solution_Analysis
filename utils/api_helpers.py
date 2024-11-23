import requests
import base64
import os

def call_google_model(image_data):
    """Call Google Generative AI model (placeholder)."""
    # Replace with actual API call logic
    return {"response": "Google AI Output"}

def call_openai_model(image_data):
    """Call OpenAI model (placeholder)."""
    # Replace with actual API call logic
    return {"response": "OpenAI Output"}

def save_to_github(file_path, content):
    """Save output to GitHub repository."""
    from github import Github

    # Authenticate using a personal access token
    token = os.getenv("GITHUB_TOKEN")  # Store in environment variable
    g = Github(token)

    # Specify repo and file details
    repo = g.get_repo("forittik/questionpaper_and_solution_analysis")
    file = repo.get_contents(file_path)
    content = json.dumps(content, indent=2)
    if file:  # Update file
        repo.update_file(file.path, "Update output", content, file.sha)
    else:  # Create new file
        repo.create_file(file_path, "Add output", content)
