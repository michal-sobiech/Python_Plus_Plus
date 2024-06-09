from project.parser.ast_nodes.node.PositionNodeABC import PositionNodeABC

from project.parser.ast_nodes.StatementABC import StatementABC

from project.PositionInCode import PositionInCode


class Block(PositionNodeABC):
    def __init__(
        self,
        position: PositionInCode,
        statements: list[StatementABC]
    ) -> None:
        super().__init__(position)
        self.statements = statements

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_block(self)
