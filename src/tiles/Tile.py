from PIL import Image

from src.cells.direction import Direction


ALLOWED_ROTATION_DIRECTIONS = set(['left', 'right'])


class Tile:
    def __init__(self, image: Image.Image|None = None, match_code: str = '------------'):
        '''
        - image - Image as specified by PIL
        - side_codes - tuple with each position corresponds to tile side direction (North, East, South, West)
        '''
        self.image = image
        self.match_code = match_code


    def __repr__(self) -> str:
        return f'<image={self.image}, side_code={self.match_code}>'


    def rotate_tile(self, rotations: int = 0, rotate_direction: str = 'left') -> bool:
        '''
        Rotates @image and shifts @match_code.

        - rotations - number of rotation applied to @tile
        - rotate_direction - direction, counter-clockwise(left) or clockwise(right), to rotate @tile

        Valid direction values: left, right
        '''
        if rotate_direction not in ALLOWED_ROTATION_DIRECTIONS:
            raise ValueError(f'Invalid rotate_direction: {rotate_direction}; Can only be left or right')

        if self.image is not None:
            self.image = self.__rotate_image(rotations, rotate_direction)
            self.match_code = self.__shift_match_code(rotations, rotate_direction)
            return True

        return False


    def __rotate_image(self, rotations: int = 0, rotate_direction: str = 'left') -> Image.Image:
        '''
        Rotates @image by 90 * (rotations % 4) degrees.

        - rotations - number of rotation applied to @image
        - rotate_direction - direction, counter-clockwise(left) or clockwise(right), to rotate @image

        Valid rotate_direction values: left, right
        '''
        angle = 90 * (rotations % 4)
        angle *= +1 if rotate_direction == 'left' else -1
        return self.image.rotate(angle)


    def __shift_match_code(self, shifts = 0, shift_direction: str = 'left') -> str:
        '''
        Shifts @side_codes.

        - shifts - number of shifts applied to @match_code
        - shift_direction - direction, left or right, to shift @match_code

        Valid direction values: left, right
        '''
        shifted_match_code = str(self.match_code)
        for _ in range(shifts):
            shifted_match_code = self.__shift_match_code_once(shifted_match_code, shift_direction)
        return shifted_match_code


    def __shift_match_code_once(self, code_to_shift: str, shift_direction = 'left') -> str:
        if shift_direction == 'left':
            return code_to_shift[3:12] + code_to_shift[0:3]
        else:
            return code_to_shift[9:12] + code_to_shift[0:9]


    def get_image_size(self) -> None|int:
        '''
        If @image is None, returns None.
        Otherwise returns size of image.
        '''
        if self.image is None:
            return None
        
        return self.image._size[0]


    def resize_image(self, new_size: int) -> bool:
        '''
        Resizes @image.

        - new_size - new size of image after resizing
        '''
        if self.image is not None:
            self.image = self.image.resize((new_size, new_size))
            return True

        return False


    def does_side_code_match(self, other: 'Tile', direction: Direction) -> bool:
        '''
        Checks if self.side_codes[opposite_direction] == other.side_codes[direction]
        
        - other - tile to witch self is compared
        - direction - Direction on which to compare side_codes
        '''
        if isinstance(direction, Direction) is False:
            raise TypeError('direction must be of type \'Direction\'')

        if not direction.is_valid():
            raise ValueError('Invalid direction.')
        
        opposite_direction = direction.get_opposite()
        return self.match_code[opposite_direction.get_slice()] == other.match_code[direction.get_slice()][::-1]
