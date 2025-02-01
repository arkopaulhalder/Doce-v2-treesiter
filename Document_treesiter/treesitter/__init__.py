from constants import Language
from treesitter.treesitter import DynamicTreesitter

def create_treesitter(language: Language) -> DynamicTreesitter:
    """Creates and returns a DynamicTreesitter instance for the given language."""
    return DynamicTreesitter(language)
