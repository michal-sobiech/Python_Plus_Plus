from __future__ import annotations


class PositionInCode:
    def __init__(
        self,
        row_no: int,
        column_no: int
    ) -> None:
        self.row_no = row_no
        self.column_no = column_no

    def __eq__(self, other: PositionInCode) -> bool:
        return (
            self.row_no == other.row_no
            and self.column_no == other.column_no
        )
