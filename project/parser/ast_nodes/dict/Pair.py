from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class Pair(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        key: ExpressionABC,
        value: ExpressionABC
    ) -> None:
        super().__init__(position)
        self.key = key
        self.value = value

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_pair(self)