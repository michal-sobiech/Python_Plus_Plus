from abc import ABC, abstractmethod

# from project.interpreter.nodes.variable.Variable import Variable
# from project.interpreter.nodes.function.EmbeddedFunction import EmbeddedFunction


class StructABC(ABC):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
