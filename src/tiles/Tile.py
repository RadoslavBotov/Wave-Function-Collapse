
'''
Tile object implementation
'''
from PIL import Image
from src.cells.direction import Direction


ALLOWED_ROTATION_DIRECTIONS = set(['left', 'right'])


class Tile:
    def __init__(self, image: Image.Image|None = None, sides_code: str = '!!!!!!!!!!!!'):
        '''
        - image - Image as specified by PIL module
        - sides_code - a 12 character long string, divided into 4 groups of 3 consecutive characters,
                       where each group represents a code for one side of the image (north, east, south, west)
                       starting from left to right: 'aaa bbb ccc ddd'
        '''
        self.image = image
        self.sides_code = sides_code


    def __repr__(self) -> str:
        return f'<image={self.image}, sides_code={self.sides_code}>'


    def rotate_tile(self, rotations: int = 0, rotate_direction: str = 'left') -> None:
        '''
        Rotates @image(if tile has one) and shifts @sides_code.

        - rotations - number of rotations
        - rotate_direction - rotating direction, counter-clockwise(left) or clockwise(right)

        Valid direction values: left, right
        '''
        if rotate_direction not in ALLOWED_ROTATION_DIRECTIONS:
            raise ValueError(f'Invalid rotate_direction: {rotate_direction}; Can only be left or right')

        self.image = self.__get_rotated_image(rotations, rotate_direction)
        self.sides_code = self.__get_shifted_sides_code(rotations * 3, rotate_direction)


    def __get_rotated_image(self, rotations: int = 0, rotate_direction: str = 'left') -> None|Image.Image:
        '''
        Rotates @image by 90 * (rotations % 4) degrees.
        If tile has @image, returns copy of rotated image, otherwise None.

        - rotations - number of rotations
        - rotate_direction - rotating direction, counter-clockwise(left) or clockwise(right)

        Valid rotate_direction values: left, right
        '''
        if self.image is not None:
            rotation_angle = 90 * (rotations % 4)
            rotation_angle *= -1 if rotate_direction == 'right' else +1
            rotated_image = self.image.rotate(rotation_angle)
            
            return rotated_image

        return None


    def __get_shifted_sides_code(self, shifts = 0, shift_direction: str = 'left') -> str:
        '''
        Shifts @sides_code with wrap-around (first character becomes last and vice versa).

        - shifts - number of shifts
        - shift_direction - shifts direction, left or right

        If sides_code is '123': `__get_shifted_sides_code(1, 'left') returns '231'`
        `__get_shifted_sides_code(2, 'left') returns '312'`

        Valid direction values: left, right
        '''
        shifts *= -1 if shift_direction == 'right' else +1
        shifted_sides_code = self.sides_code[shifts:] + self.sides_code[:shifts]
        
        return shifted_sides_code


    def get_image_size(self) -> tuple[int, int]|None:
        '''
        If tile has @image, returns its size as a tuple (width, height).
        Otherwise, returns None.
        '''
        if self.image is None:
            return None
        
        return self.image._size


    def resize_image(self, new_size: tuple[int, int]) -> bool:
        '''
        Resizes @image.
        Returns True if tile has @image and resize succeeds.
        Otherwise, returns False.

        - new_size - new size of image after resizing
        '''
        if self.image is None:
            return False

        if self.get_image_size() != new_size:
            self.image = self.image.resize(new_size)

        return True


    def does_sides_code_match(self, other: 'Tile', direction: Direction) -> bool:
        '''
        Checks if sides_code along a shared side of two touching tiles match.
        Returns true if sides_code match, and false, otherwise.

        - other - other tile with which sides_code is matched
        - direction - Direction of others' side to match self to

        If we want to compare Tile@selfs NORTH side to Tile@other SOUTH side, direction should be SOUTH.
        '''
        if isinstance(direction, Direction) is False:
            raise TypeError('direction must be of type \'Direction\'')

        if direction.is_invalid():
            raise ValueError('Invalid direction.')

        opposite_direction = direction.get_opposite()

        self_side_slice = opposite_direction.get_slice()
        other_side_slice = direction.get_slice(reverse=True)

        return self.sides_code[self_side_slice] == other.sides_code[other_side_slice]
