"""Python example"""

def simple_function():
    """A simple Python function"""
    return "Hello from Python :D"

class TestClass:
    def __init__(self, name: str):
        """Constructor"""
        self.name = name

    def greet(self) -> str:
        """Return a greeting"""
        return f"Hello, {self.name}!"
