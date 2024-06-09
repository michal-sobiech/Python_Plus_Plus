from project.parser.ast_nodes.dict.DictElement import DictElement
from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class Dict(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        elements: list[DictElement]
    ) -> None:
        super().__init__(position)
        self.elements = elements

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_dict(self)
