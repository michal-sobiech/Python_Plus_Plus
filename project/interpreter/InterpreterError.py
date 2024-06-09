from project.PositionInCode import PositionInCode
from project.interpreter.InterpreterErrorMsg import InterpreterErrorMsg
from project.interpreter.nodes.Context import Context


class InterpreterError(Exception):
    def __init__(
        self,
        position: PositionInCode,
        description: InterpreterErrorMsg,
        function_call_contexts: list[Context]
    ) -> None:
        super().__init__()
        self.position = position
        self.description = description
        self.function_call_contexts = function_call_contexts
