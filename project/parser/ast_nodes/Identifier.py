from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class Identifier(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        value: str
    ) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_identifier(self)