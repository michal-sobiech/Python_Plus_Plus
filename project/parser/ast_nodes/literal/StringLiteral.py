from project.parser.ast_nodes.literal.LiteralABC import LiteralABC

from project.PositionInCode import PositionInCode


class StringLiteral(LiteralABC):
    def __init__(
        self,
        position: PositionInCode,
        value: str
    ) -> None:
        super().__init__(position, value)

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_string_literal(self)
