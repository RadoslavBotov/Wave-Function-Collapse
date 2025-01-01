from dataclasses import dataclass


@dataclass
class HighlightData:
    def __init__(self, last_row = -1, last_column = -1, last_rect = None):
        self.last_row = last_row
        self.last_column = last_column
        self.last_rect = last_rect