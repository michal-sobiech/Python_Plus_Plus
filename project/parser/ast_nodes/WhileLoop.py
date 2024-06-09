from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.parser.ast_nodes.Block import Block

from project.parser.ast_nodes.StatementABC import StatementABC

from project.PositionInCode import PositionInCode


class WhileLoop(StatementABC):
    def __init__(
        self,
        position: PositionInCode,
        condition: ExpressionABC,
        body: Block
    ) -> None:
        super().__init__(position)
        self.condition = condition
        self.body = body

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_while_loop(self)
