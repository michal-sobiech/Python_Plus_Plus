from abc import abstractmethod

from project.parser.ast_nodes.node.NodeABC import NodeABC

from project.PositionInCode import PositionInCode


class PositionNodeABC(NodeABC):
    @abstractmethod
    def __init__(
        self,
        position: PositionInCode
    ) -> None:
        super().__init__()
        self.position = position
