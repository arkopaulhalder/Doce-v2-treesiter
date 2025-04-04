
import os
import requests
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv('LLAMA-90B_API_KEY')
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def extract_file_content(file_path):
    """Reads and returns the content of the Java file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
def generate_documentation(file_content):
    """Generates documentation for the given Java file content."""
    if not OPENROUTER_API_KEY:
        return "Error: API key not configured"

    try:
        prompt = f"""
Analyze the following Java code and generate detailed documentation for its classes, methods, and other constructs.
In human-readable format. Use descriptive language/paragraphs to explain the purpose of each function, its parameters, return values, and functionality.
Provide clear descriptions of:
- The purpose of the class.
- The functionality of each method.
- The parameters, return values, and any important logic.

{file_content}
"""
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-3.2-90b-vision-instruct:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises exception for 4XX/5XX status codes
        result = response.json()
        if 'choices' in result and result['choices']:
            return result['choices'][0]['message']['content']
        return "Error: Invalid response format from API"

    except requests.exceptions.RequestException as e:
        return f"Error making API request: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def process_java_repository(directory_path):
    """Processes all Java files in the directory, generates documentation, and consolidates the results."""
    result = {"files": []}

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                try:
                    file_content = extract_file_content(file_path)
                    documentation = generate_documentation(file_content)
                    if documentation:
                        result["files"].append({
                            "file_path": file_path,
                            "documentation": documentation
                        })
                    else:
                        result["files"].append({
                            "file_path": file_path,
                            "error": "Failed to generate documentation."
                        })
                except Exception as e:
                    result["files"].append({
                        "file_path": file_path,
                        "error": str(e)
                    })

    return result
    
@app.route('/')
def home():
    return "Flask server is running and ready to accept requests!"

@app.route('/generate-docs', methods=['POST'])
def generate_docs():
    """API endpoint to generate documentation for all Java files in a directory."""
    try:
        data = request.json
        directory_path = data.get("directory_path")
        if not directory_path or not os.path.exists(directory_path):
            return jsonify({"error": "Invalid or non-existent directory path."}), 400
        
        result = process_java_repository(directory_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Flask server is running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)