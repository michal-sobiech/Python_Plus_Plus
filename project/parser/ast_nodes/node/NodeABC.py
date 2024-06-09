from __future__ import annotations

from abc import ABC, abstractmethod


class NodeABC(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    def __eq__(self, other: NodeABC) -> bool:
        if type(self) is not type(other):
            return NotImplemented

        # return self.__dict__ == other.__dict__

        # are_equal = (
        #     super().__eq__(other)
        #     and self.__dict__ == other.__dict__
        # )

        are_equal = True
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                # print("AAAAAAAaa", type(self), key, self.__dict__[key], other.__dict__[key])
                print("AAAAAAAaa", type(self), key, self.__dict__[key], other.__dict__[key])
                are_equal = False

        # are_equal = self.__dict__ == other.__dict__

        # print('-------------')
        # print(are_equal)
        # print(type(self))
        # print('self dict: ', self.__dict__)
        # print('other dict:', other.__dict__)

        return are_equal
