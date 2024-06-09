from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.parser.ast_nodes.StatementABC import StatementABC

from project.parser.ast_nodes.Identifier import Identifier

from project.parser.ast_nodes.Block import Block

from project.PositionInCode import PositionInCode


class ForLoop(StatementABC):
    def __init__(
        self,
        position: PositionInCode,
        iterator_var: Identifier,
        sequence: ExpressionABC,
        body: Block
    ) -> None:
        super().__init__(position)
        self.iterator_var = iterator_var
        self.sequence = sequence
        self.body = body

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_for_loop(self)
