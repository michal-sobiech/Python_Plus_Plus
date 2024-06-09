from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.parser.ast_nodes.StatementABC import StatementABC

from project.PositionInCode import PositionInCode


class Assignment(StatementABC):
    def __init__(
        self,
        position: PositionInCode,
        left_expression: ExpressionABC,
        right_expression: ExpressionABC
    ) -> None:
        super().__init__(position)
        self.left_expression = left_expression
        self.right_expression = right_expression

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_assignment(self)
