from project.parser.ast_nodes.operator_terms.comparison_term.CompTermABC import CompTermABC

from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class GreaterEqualTerm(CompTermABC):
    def __init__(
        self,
        position: PositionInCode,
        left_term: ExpressionABC,
        right_term: ExpressionABC
    ) -> None:
        super().__init__(position, left_term, right_term)

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_greater_equal_terms(self)
