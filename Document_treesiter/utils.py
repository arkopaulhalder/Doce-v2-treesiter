import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from tree_sitter import Parser
from typing import Dict
from treesitter.treesitter import DynamicTreesitter
from tree_sitter import Language, Parser as TreeParser

def create_treesitter(language: Language) -> DynamicTreesitter:
    """Creates and returns a DynamicTreesitter instance for the given language."""
    return DynamicTreesitter(language)



try:
    from tree_sitter import Language, Parser as TreeParser
    
    from tree_sitter_languages import get_parser
    TREE_SITTER_AVAILABLE = True
except ImportError:
    print("Warning: tree-sitter not installed. Please install with: pip install tree-sitter tree-sitter-languages")
    TREE_SITTER_AVAILABLE = False
    tree_sitter_parser = None
    get_parser = None

from constants import Language as LangEnum
from treesitter import create_treesitter

class LanguageHandler:
    _instance = None
    _parsers: Dict[LangEnum, Optional[TreeParser]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._parsers:
            self._initialize_parsers()
    
    def _initialize_parsers(self):
        if not TREE_SITTER_AVAILABLE:
            return
        
        language_mapping = {
            LangEnum.PYTHON: 'python',
            LangEnum.JAVASCRIPT: 'javascript',
            LangEnum.TYPESCRIPT: 'typescript',
            LangEnum.JAVA: 'java',
            LangEnum.CPP: 'cpp',
            LangEnum.C: 'c',
            LangEnum.HTML: 'html',
            LangEnum.CSS: 'css',
            LangEnum.PHP: 'php',
            LangEnum.RUBY: 'ruby',
            LangEnum.GO: 'go',
            LangEnum.RUST: 'rust',
            LangEnum.SWIFT: 'swift',
            LangEnum.KOTLIN: 'kotlin',
            LangEnum.C_SHARP: 'csharp',
            LangEnum.OBJECTIVE_C: 'objc',
            LangEnum.SCALA: 'scala',
            LangEnum.PERL: 'perl',
            LangEnum.LUA: 'lua',
            LangEnum.R: 'r'
        }
        
        for lang_enum, lang_name in language_mapping.items():
            if get_parser is None:
                print(f"Warning: get_parser is not available for {lang_name}")
                continue
            try:
                parser = get_parser(lang_name)
                #print(parser)
                self._parsers[lang_enum] = parser
            except Exception as e:
                print(f"Warning: Failed to initialize parser for {lang_name}: {e}")
    
    def get_parser(self, language: LangEnum) -> Optional[TreeParser]:
        return self._parsers.get(language)

def get_programming_language(file_extension: str) -> LangEnum:
    """Returns the programming language based on file extension."""
    language_mapping = {
        ".py": LangEnum.PYTHON,
        ".js": LangEnum.JAVASCRIPT,
        ".jsx": LangEnum.JAVASCRIPT,
        ".ts": LangEnum.TYPESCRIPT,
        ".tsx": LangEnum.TYPESCRIPT,
        ".java": LangEnum.JAVA,
        ".cpp": LangEnum.CPP,
        ".hpp": LangEnum.CPP,
        ".c": LangEnum.C,
        ".h": LangEnum.C,
        ".html": LangEnum.HTML,
        ".htm": LangEnum.HTML,
        ".css": LangEnum.CSS,
        ".php": LangEnum.PHP,
        ".rb": LangEnum.RUBY,
        ".go": LangEnum.GO,
        ".rs": LangEnum.RUST,
        ".swift": LangEnum.SWIFT,
        ".kt": LangEnum.KOTLIN,
        ".cs": LangEnum.C_SHARP,
        ".m": LangEnum.OBJECTIVE_C,
        ".mm": LangEnum.OBJECTIVE_C,
        ".scala": LangEnum.SCALA,
        ".pl": LangEnum.PERL,
        ".lua": LangEnum.LUA,
        ".r": LangEnum.R
    }
    return language_mapping.get(file_extension.lower(), LangEnum.UNKNOWN)

def get_file_extension(file_path: str) -> str:
    """Returns the file extension from a path."""
    return Path(file_path).suffix.lower()

def process_file_content(file_path: str, parser: TreeParser) -> Tuple[Optional[List[dict]], Optional[str]]:
    if not TREE_SITTER_AVAILABLE:
        return None, "tree-sitter is not installed"
        
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        language = get_programming_language(get_file_extension(file_path))
        treesitter = create_treesitter(language)
        parsed_methods = treesitter.parse(content)
        
        return parsed_methods, None
        
    except Exception as e:
        return None, f"Error processing file: {str(e)}"

def process_repository(directory_path: str, language: LangEnum) -> dict:
    if not TREE_SITTER_AVAILABLE:
        return {"error": "tree-sitter is not installed. Please install with: pip install tree-sitter tree-sitter-languages"}
        
    result = {"files": []}
    
    if not os.path.exists(directory_path):
        return {"error": f"Directory not found: {directory_path}"}
        
    language_handler = LanguageHandler()
    parser = language_handler.get_parser(language)
    
    if not parser:
        return {"error": f"No parser available for language: {language.value}"}
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if get_programming_language(get_file_extension(file)) == language:
                file_path = os.path.join(root, file)
                parsed_methods, error = process_file_content(file_path, parser)
                
                if error:
                    result["files"].append({
                        "file_path": file_path,
                        "error": error
                    })
                    continue
                    
                result["files"].append({
                    "file_path": file_path,
                    "methods": [
                        {
                            "name": method.name,
                            "doc_comment": method.doc_comment,
                            "source_code": method.method_source_code,
                            "start_line": method.start_line,
                            "end_line": method.end_line
                        }
                        for method in parsed_methods
                    ] if parsed_methods else []
                })
    
    return result