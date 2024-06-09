from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class DotTerm(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        terms: list[ExpressionABC]
    ) -> None:
        super().__init__(position)
        self.terms = terms

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_dot_term(self)