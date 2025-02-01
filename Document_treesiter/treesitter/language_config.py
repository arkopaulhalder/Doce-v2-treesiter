
from dataclasses import dataclass
from constants import Language

@dataclass
class LanguageConfig:
    method_identifier: str
    name_identifier: str
    comment_identifier: str
    docstring_query: str = None

LANGUAGE_CONFIGS = {
    Language.PYTHON: LanguageConfig(
        "function_definition",
        "identifier",
        "comment",
        "(function_definition body: (block . (expression_statement (string)) @docstring))"
    ),
    Language.JAVASCRIPT: LanguageConfig(
        "function_declaration",
        "identifier",
        "comment"
    ),
    Language.TYPESCRIPT: LanguageConfig(
        "function_declaration",
        "identifier",
        "comment"
    ),
    Language.JAVA: LanguageConfig(
        "method_declaration",
        "identifier",
        "block_comment"
    ),
    Language.CPP: LanguageConfig(
        "function_definition",
        "function_declarator",
        "comment"
    ),
    Language.C: LanguageConfig(
        "function_definition",
        "function_declarator",
        "comment"
    ),
    Language.GO: LanguageConfig(
        "function_declaration",
        "identifier",
        "comment"
    ),
    Language.RUST: LanguageConfig(
        "function_item",
        "identifier",
        "line_comment"
    ),
    Language.KOTLIN: LanguageConfig(
        "function_declaration",
        "simple_identifier",
        "comment"
    ),
    Language.C_SHARP: LanguageConfig(
        "method_declaration",
        "identifier",
        "comment"
    )
}
