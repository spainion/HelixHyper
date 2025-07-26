"""Agent that executes Python code using the python interpreter plugin."""

from .base_agent import BaseAgent
from plugins.python_interpreter import PythonInterpreter


class CodeAgent(BaseAgent):
    """Execute arbitrary Python code and return the captured stdout."""

    def __init__(self) -> None:
        self.interpreter = PythonInterpreter()

    def act(self, prompt: str) -> str:  # type: ignore[override]
        return self.interpreter.execute(prompt)