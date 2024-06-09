from typing import Iterator
from io import TextIOBase


class CodeSource():
    __slots__ = [
        '_file_handle',
        'char_abs_no',
        'char_row_no',
        'char_column_no',
        '_reached_end'
    ]

    def __init__(
        self,
        file_handle: TextIOBase
    ) -> None:
        self._file_handle = file_handle
        self.char_abs_no = 0
        self.char_row_no = 1
        self.char_column_no: int = None
        self.reset_char_column_no()

        self._reached_end = False

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        char = self._file_handle.read(1)

        if char == '\n':
            self.char_row_no += 1
            self.reset_char_column_no()
            return char

        elif char in '' and self._reached_end:
            raise StopIteration

        else:
            self.char_abs_no += 1
            self.char_column_no += 1
            if char in '' and not self._reached_end:
                self._reached_end = True
                raise StopIteration
            return char

    def reset_char_column_no(self) -> None:
        self.char_column_no = 0
