from project.parser.ast_nodes.literal.LiteralABC import LiteralABC

from project.PositionInCode import PositionInCode


class BoolLiteral(LiteralABC):
    def __init__(
        self,
        position: PositionInCode,
        value: bool
    ) -> None:
        super().__init__(position, value)

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_bool_literal(self)
