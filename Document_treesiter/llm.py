import os
import time
import requests
from typing import Optional, Dict, List
from dotenv import load_dotenv
from treesitter.treesitter import TreesitterMethodNode

load_dotenv()

class LLM:
    def __init__(
        self,
        api_key: str = None,
        model: str = "gemini-pro",
        max_tokens: int = 1000,
        max_retries: int = 3,
        retry_delay: int = 1
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided and not found in environment")
            
        self.api_endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
        self.model = model
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Template for whole file documentation
        self.file_template = """
        Analyze the following {language} code and generate detailed documentation.
        
        Instructions:
        1. Document the overall purpose of the code
        2. For each class/function:
           - Description of purpose and functionality
           - Parameters and their types
           - Return values and types
           - Key algorithms or logic
           - Usage examples where helpful
        3. Note any important dependencies or requirements
        4. {inline_comments}
        
        Code to document:
        {code}
        """
        
        # Template for method-level documentation
        self.method_template = """
        Analyze the following {language} method and generate detailed documentation.
        
        Method Name: {method_name}
        
        Documentation Comments: 
        {doc_comment}
        
        Method Source Code:
        {method_source}
        
        Instructions:
        1. Document this method's purpose and functionality
        2. Parameters and their types
        3. Return values and types
        4. Key algorithms or logic
        5. Usage examples where helpful
        6. Any important dependencies or requirements
        """

    def call_gemini_api(self, prompt: str) -> Optional[str]:
        headers = {"Content-Type": "application/json"}
        
        # Fixed payload structure according to Gemini API requirements
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "maxOutputTokens": self.max_tokens,
                "temperature": 0.3,
                "topP": 0.8,
                "topK": 40
            }
        }

        params = {
            "key": self.api_key
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_endpoint,
                    params=params,
                    json=payload,
                    headers=headers,
                    timeout=30 # Adding timeout
                )
                
                if response.status_code == 400:
                    print(f"API Error Response: {response.text}")
                    if attempt == self.max_retries - 1:
                        return "Error: Invalid request format"
                    continue
                    
                response.raise_for_status()
                
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        return candidate['content']['parts'][0].get('text', '')
                
                print(f"Unexpected API response: {result}")
                return None

            except requests.exceptions.RequestException as e:
                print(f"API request error (attempt {attempt + 1}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return f"Error: API request failed - {str(e)}"
                time.sleep(self.retry_delay * (attempt + 1))
                
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return f"Error: {str(e)}"

    def generate_documentation(self, language: str, code: str, inline_comments: str = "") -> str:
        """Generate documentation for a complete file."""
        try:
            prompt = self.file_template.format(
                language=language,
                code=code,
                inline_comments="Include inline comments in the documentation." if inline_comments else "Focus on code structure and functionality."
            )
            
            documentation = self.call_gemini_api(prompt)
            if not documentation:
                return "Failed to generate documentation."
                
            return documentation
            
        except Exception as e:
            return f"Error generating documentation: {str(e)}"

    def generate_structured_documentation(self, language: str, methods: List[TreesitterMethodNode]) -> Dict[str, str]:
        documentation = {}
        try:
            for method in methods:
                if not method.get("name"):
                    continue
                    
                prompt = self.method_template.format(
                    language=language,
                    method_name=method["name"],
                    doc_comment=method.get("doc_comment", "No documentation provided"),
                    method_source=method.get("source_code", "")
                )
                
                method_doc = self.call_gemini_api(prompt)
                if method_doc and not method_doc.startswith("Error:"):
                    documentation[method["name"]] = method_doc
                else:
                    documentation[method["name"]] = "Failed to generate documentation: " + (method_doc or "Unknown error")
                
            return documentation
            
        except Exception as e:
            print(f"Documentation generation error: {str(e)}")
            return {"error": f"Error generating structured documentation: {str(e)}"}