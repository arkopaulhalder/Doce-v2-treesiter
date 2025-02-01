from typing import Optional, List
import tree_sitter
from tree_sitter_languages import get_language
from constants import Language
from treesitter.language_config import LANGUAGE_CONFIGS, LanguageConfig

class TreesitterMethodNode:
    def __init__(self, name: str, doc_comment: str, method_source_code: str, 
                 start_line: int, end_line: int):
        self.name = name
        self.doc_comment = doc_comment
        self.method_source_code = method_source_code
        self.start_line = start_line
        self.end_line = end_line

class DynamicTreesitter:
    def __init__(self, language: Language):
        self.language = language
        self.config = LANGUAGE_CONFIGS.get(language)
        if not self.config:
            raise ValueError(f"Unsupported language: {language}")
            
        self.parser = tree_sitter.Parser()
        try:
            lang = get_language(language.value)
            self.parser.set_language(lang)
        except Exception as e:
            raise ValueError(f"Failed to set language {language.value}: {str(e)}")
        
        if self.config.docstring_query:
            try:
                self._doc_query = self.parser.language.query(self.config.docstring_query)
            except Exception:
                self._doc_query = None
        else:
            self._doc_query = None

    def parse(self, source_bytes: bytes) -> List[TreesitterMethodNode]:
        """Parse source code and extract method information."""
        try:
            tree = self.parser.parse(source_bytes)
            return self._extract_methods(tree.root_node)
        except Exception as e:
            raise Exception(f"Failed to parse source code: {str(e)}")

    def _extract_methods(self, root_node: tree_sitter.Node) -> List[TreesitterMethodNode]:
        """Extract method information from the parsed syntax tree."""
        methods = []
        for node in self._query_all_methods(root_node):
            method_name = self._query_method_name(node)
            if method_name:
                doc_comment = self._query_doc_comment(node)
                source_code = node.text.decode('utf-8')
                methods.append(TreesitterMethodNode(
                    name=method_name,
                    doc_comment=doc_comment,
                    method_source_code=source_code,
                    start_line=node.start_point[0],
                    end_line=node.end_point[0]
                ))
        return methods

    def _query_all_methods(self, node: tree_sitter.Node) -> List[tree_sitter.Node]:
        """Find all method nodes in the syntax tree."""
        methods = []
        if node.type == self.config.method_identifier:
            methods.append(node)
        for child in node.children:
            methods.extend(self._query_all_methods(child))
        return methods

    def _query_method_name(self, node: tree_sitter.Node) -> Optional[str]:
        """Extract method name from a method node."""
        if self.language in [Language.CPP, Language.C]:
            for child in node.children:
                if child.type == "function_declarator":
                    for subchild in child.children:
                        if subchild.type == "identifier":
                            return subchild.text.decode()
        else:
            for child in node.children:
                if child.type == self.config.name_identifier:
                    return child.text.decode()
        return None

    def _query_doc_comment(self, node: tree_sitter.Node) -> Optional[str]:
        """Extract documentation comments for a method."""
        if self._doc_query:  # Python-style docstrings
            captures = self._doc_query.captures(node)
            if captures:
                return captures[0][0].text.decode('utf-8')
        
        # Regular comments
        prev_sibling = node.prev_named_sibling
        if prev_sibling and prev_sibling.type == self.config.comment_identifier:
            return prev_sibling.text.decode('utf-8')
        return None
