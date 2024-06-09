from project.parser.ast_nodes.return_statement.ReturnABC import ReturnABC

from project.PositionInCode import PositionInCode


class ReturnNoValue(ReturnABC):
    def __init__(
        self,
        position: PositionInCode
    ) -> None:
        super().__init__(position)

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_return_no_value(self)
