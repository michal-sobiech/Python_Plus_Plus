from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.parser.ast_nodes.incr_decr_statement.IncrDecrStatementABC import IncrDecrStatementABC

from project.PositionInCode import PositionInCode


class DecrementStatement(IncrDecrStatementABC):
    def __init__(
        self,
        position: PositionInCode,
        expression: ExpressionABC
    ) -> None:
        super().__init__(position, expression)

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_decrement_statement(self)
