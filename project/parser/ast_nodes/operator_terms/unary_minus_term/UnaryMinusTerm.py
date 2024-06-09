from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.parser.ast_nodes.operator_terms.DotTerm import DotTerm

from project.PositionInCode import PositionInCode


class UnaryMinusTerm(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        term: ExpressionABC
    ) -> None:
        super().__init__(position)
        self.term = term

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_unary_minus_term(self)
