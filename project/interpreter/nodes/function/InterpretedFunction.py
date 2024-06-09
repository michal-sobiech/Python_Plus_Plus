from project.interpreter.nodes.function.FunctionABC import FunctionABC


class InterpretedFunction(FunctionABC):
    def __init__(
        self,
        name: str,
        parameters: list[str],
        body
    ) -> None:
        super().__init__(name, parameters)
        self.body = body

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_interpreted_function(self)
