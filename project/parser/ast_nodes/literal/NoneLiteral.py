from project.parser.ast_nodes.literal.LiteralABC import LiteralABC

from project.PositionInCode import PositionInCode


class NoneLiteral(LiteralABC):
    def __init__(
        self,
        position: PositionInCode
    ) -> None:
        super().__init__(position, None)

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_none_literal(self)
