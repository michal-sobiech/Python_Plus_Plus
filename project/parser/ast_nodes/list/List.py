from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class List(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        elements: list[ExpressionABC]
    ) -> None:
        super().__init__(position)
        self.elements = elements

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_list(self)
