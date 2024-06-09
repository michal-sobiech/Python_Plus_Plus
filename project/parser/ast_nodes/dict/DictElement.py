from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC
from project.parser.ast_nodes.node.PositionNodeABC import PositionNodeABC
from project.PositionInCode import PositionInCode


class DictElement(PositionNodeABC):
    def __init__(
        self,
        position: PositionInCode,
        key: ExpressionABC,
        value: ExpressionABC
    ) -> None:
        super().__init__(position)
        self.key = key
        self.value = value

    def accept(self, intepreter_visitor) -> None:
        intepreter_visitor.visit_dict_element(self)
