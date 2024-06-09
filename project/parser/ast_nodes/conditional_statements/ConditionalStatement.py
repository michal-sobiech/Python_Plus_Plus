from typing import Optional

from project.parser.ast_nodes.node.NodeABC import NodeABC
from project.parser.ast_nodes.StatementABC import StatementABC

from project.parser.ast_nodes.conditional_statements.IfStatement import IfStatement
from project.parser.ast_nodes.conditional_statements.ElifStatement import ElifStatement
from project.parser.ast_nodes.conditional_statements.ElseStatement import ElseStatement

from project.PositionInCode import PositionInCode


class ConditionalStatement(StatementABC):
    def __init__(
        self,
        position: PositionInCode,
        if_statement: IfStatement,
        elif_statements: list[ElifStatement],
        else_statement: Optional[ElseStatement],
    ) -> None:
        super().__init__(position)
        self.if_statement = if_statement
        self.elif_statements = elif_statements
        self.else_statement = else_statement

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_conditional_statement(self)
