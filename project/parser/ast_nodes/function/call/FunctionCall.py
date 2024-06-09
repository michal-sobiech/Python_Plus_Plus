from __future__ import annotations

from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.parser.ast_nodes.Identifier import Identifier

from project.PositionInCode import PositionInCode


class FunctionCall(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        function_name: Identifier,
        args: list[ExpressionABC]
    ) -> None:
        super().__init__(position)
        self.function_name = function_name
        self.args = args

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_function_call(self)
