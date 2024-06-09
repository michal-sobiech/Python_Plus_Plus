from project.parser.ast_nodes.node.PositionNodeABC import PositionNodeABC
from project.parser.ast_nodes.Block import Block
from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class IfStatement(PositionNodeABC):
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
        interpreter_visitor.visit_if_statement(self)
