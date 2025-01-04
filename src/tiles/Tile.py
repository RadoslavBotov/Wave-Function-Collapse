from PIL import Image

from src.cells.direction import Direction


ALLOWED_ROTATION_DIRECTIONS = set(['left', 'right'])


class Tile:
    def __init__(self, image: Image.Image|None = None, side_codes: tuple[int, int, int, int] = (-1, -1, -1, -1)):
        '''
        - image - Image as specified by PIL
        - side_codes - tuple with each position corresponds to tile side direction (North, East, South, West)
        '''
        self.image = image
        self.side_codes = side_codes


    def __repr__(self) -> str:
        return f'<image={self.image}, side_codes={self.side_codes}>'


    def rotate_tile(self, rotations: int = 0, rotate_direction: str = 'left') -> bool:
        '''
        Rotates @image and shifts @side_codes.

        - rotations - number of rotation applied to @image
        - rotate_direction - direction, counter-clockwise(left) or clockwise(right), in which @image is rotated 

        Valid direction values: left, right
        '''
        if rotate_direction not in ALLOWED_ROTATION_DIRECTIONS:
            raise ValueError(f'Invalid rotate_direction: {rotate_direction}; Can only be left or right')

        if self.image is not None:
            self.__rotate_image(rotations, rotate_direction)
            self.__shift_permissions(rotations, rotate_direction)
            return True

        return False


    def __rotate_image(self, rotations: int = 0, rotate_direction: str = 'left') -> None:
        '''
        Rotates @image by 90 * (rotations % 4) degrees.

        - rotations - number of rotation applied to @image
        - rotate_direction - direction, counter-clockwise(left) or clockwise(right), in which @image is rotated 

        Valid rotate_direction values: left, right
        '''
        angle = 90 * (rotations % 4)
        angle *= +1 if rotate_direction == 'left' else -1
        self.image = self.image.rotate(angle)


    def __shift_permissions(self, shifts = 0, rotate_direction: str = 'left') -> None:
        '''
        Shifts @side_codes.

        - shifts - number of shifts applied to @side_codes
        - rotate_direction - direction, counter-clockwise(left) or clockwise(right), in which @image is rotated 

        Valid direction values: left, right
        '''
        shifts *= +1 if rotate_direction == 'left' else -1
        self.side_codes = self.side_codes[shifts:] + self.side_codes[:shifts]


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
        return self.side_codes[opposite_direction] == other.side_codes[direction]
