from project.parser.ast_nodes.FunDefOrStatementABC import FunDefOrStatementABC

from project.parser.ast_nodes.Block import Block
from project.parser.ast_nodes.Identifier import Identifier

from project.PositionInCode import PositionInCode


class FunctionDefinition(FunDefOrStatementABC):
    def __init__(
        self,
        position: PositionInCode,
        name: Identifier,
        parameters: list[Identifier],
        body: Block
    ) -> None:
        super().__init__(position)
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_function_definition(self)
