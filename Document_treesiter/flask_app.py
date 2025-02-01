import os
from flask import Flask, request, jsonify
from constants import Language
from utils import process_repository, get_programming_language, get_file_extension
from llm import LLM

app = Flask(__name__)
llm = LLM()

@app.route('/')
def home():
    return "Documentation Generator API is running!"

@app.route('/process', methods=['POST'])
def process():
    """Process a directory of source code files and generate documentation."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        directory = data.get("directory")
        directory = os.path.abspath(directory)
        print(f"Processing directory: {directory}")
        #print(directory)
        if not directory or not os.path.exists(directory):
            return jsonify({"error": "Invalid or non-existent directory path"}), 400

        # Initialize the results dictionary
        results = {"files": [], "stats": {"processed": 0, "failed": 0}}
        
        # Process all files in the directory
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                extension = get_file_extension(file)
                
                language = get_programming_language(extension)
                if language != Language.UNKNOWN:
                    file_result = process_repository(os.path.dirname(file_path), language)
                    
                    if "error" not in file_result:
                        for file_info in file_result["files"]:
                            methods_docs = []
                            if "methods" in file_info:
                                for method in file_info["methods"]:
                                    try:
                                        doc = llm.generate_structured_documentation(
                                            language.value,
                                            [method]
                                        )
                                        if doc and not isinstance(doc, str):
                                            method_doc = doc.get(method["name"])
                                            if method_doc and not method_doc.startswith("Error:"):
                                                results["stats"]["processed"] += 1
                                            else:
                                                results["stats"]["failed"] += 1
                                            methods_docs.append({
                                                "name": method["name"],
                                                "documentation": method_doc or "Failed to generate documentation"
                                            })
                                    except Exception as e:
                                        print(f"Error processing method {method['name']}: {str(e)}")
                                        methods_docs.append({
                                            "name": method["name"],
                                            "documentation": f"Error: {str(e)}"
                                        })
                                        results["stats"]["failed"] += 1
                                
                            results["files"].append({
                                "file_path": file_info["file_path"],
                                "language": language.value,
                                "methods": methods_docs
                            })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
