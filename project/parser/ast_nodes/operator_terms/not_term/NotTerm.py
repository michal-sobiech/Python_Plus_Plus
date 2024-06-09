from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class NotTerm(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        term: ExpressionABC
    ) -> None:
        super().__init__(position)
        self.term = term

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_not_term(self)
