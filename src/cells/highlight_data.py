from dataclasses import dataclass


@dataclass
class HighlightData:
    def __init__(self, last_row = -1, last_column = -1, last_rect = None):
        self.last_row = last_row
        self.last_column = last_column
        self.last_rect = last_rect


    def update(self, new_row: int|None = None, new_column: int|None = None, new_last_rect: int|None = None) -> None:
        '''
        Updates data. If an argument is None, previous value, of that attribute, is kept.
        '''
        self.last_row = self.last_row if new_row is None else new_row
        self.last_column = self.last_column if new_column is None else new_column
        self.last_rect = self.last_rect if new_last_rect is None else new_last_rect


    def check_match(self, row: int, column: int) -> bool:
        '''
        Returns True if @last_row and @last_column are the same as row and column, respectfully.
        otherwise, returns False.
        '''
        return self.last_row == row and self.last_column == column
