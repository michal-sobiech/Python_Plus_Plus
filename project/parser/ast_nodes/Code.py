from project.parser.ast_nodes.node.NodeABC import NodeABC

from project.parser.ast_nodes.FunDefOrStatementABC import FunDefOrStatementABC


class Code(NodeABC):
    def __init__(
        self,
        fun_defs_and_statements: list[FunDefOrStatementABC]
    ) -> None:
        super().__init__()
        self.fun_defs_and_statements = fun_defs_and_statements

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_code(self)
