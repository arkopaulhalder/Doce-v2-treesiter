from enum import Enum

class Language(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    HTML = "html"
    CSS = "css"
    PHP = "php"
    RUBY = "ruby"
    GO = "go"
    RUST = "rust"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    C_SHARP = "csharp"  # Note: using csharp instead of c_sharp for tree-sitter
    OBJECTIVE_C = "objective_c"  # Note: using objc instead of objective_c for tree-sitter
    SCALA = "scala"
    PERL = "perl"
    LUA = "lua"
    R = "r"
    UNKNOWN = "unknown"