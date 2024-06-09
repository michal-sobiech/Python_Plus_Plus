from abc import ABC, abstractmethod


class FunctionABC(ABC):
    @abstractmethod
    def __init__(
        self,
        name: str,
        parameters: list[str]
    ) -> None:
        self.name = name
        self.parameters = parameters

    def get_parameter_count(self) -> int:
        return len(self.parameters)
