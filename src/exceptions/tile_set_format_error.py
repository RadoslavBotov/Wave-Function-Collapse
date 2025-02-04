'''
Exceptions for tile sets
'''
class TileSetFormatError(Exception):
    '''
    Exception for invalid tile set configuration format when
    converting the yaml file output to program accepted input.
    '''
    def __init__(self, message = None):
        super().__init__(message)
