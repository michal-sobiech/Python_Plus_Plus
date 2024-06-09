from abc import abstractmethod

from project.parser.ast_nodes.node.PositionNodeABC import PositionNodeABC

from project.PositionInCode import PositionInCode


class FunDefOrStatementABC(PositionNodeABC):
    @abstractmethod
    def __init__(
        self,
        position: PositionInCode
    ) -> None:
        self.position = position
