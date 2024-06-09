from project.parser.ast_nodes.node.PositionNodeABC import PositionNodeABC
from project.parser.ast_nodes.Block import Block

from project.PositionInCode import PositionInCode


class ElseStatement(PositionNodeABC):
    def __init__(
        self,
        position: PositionInCode,
        body: Block
    ) -> None:
        super().__init__(position)
        self.body = body

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_else_statement(self)
