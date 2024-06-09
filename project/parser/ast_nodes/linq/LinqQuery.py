from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC
from project.parser.ast_nodes.Identifier import Identifier

from project.PositionInCode import PositionInCode


class LinqQuery(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        iterator_var: Identifier,
        source: ExpressionABC,
        condition: ExpressionABC,
        sorting_function: ExpressionABC,
        selected_values: list[ExpressionABC]
    ) -> None:
        super().__init__(position)
        self.iterator_var = iterator_var
        self.source = source
        self.condition = condition
        self.sorting_function = sorting_function
        self.selected_values = selected_values

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_linq_query(self)
