'''
Tile object implementation
'''
from PIL import Image
from src.direction import Direction


ALLOWED_ROTATION_DIRECTIONS = set(['left', 'right'])


class Tile:
    '''
    A Tile represents a rectangle with four sides (NORTH, EAST, SOUTH, WEST),
    containing an image. Each side has a 3 character long code that determines
    which other tiles can touch it on that side.
    '''
    def __init__(self, image: Image.Image|None = None, sides_code: str = '!!!!!!!!!!!!'):
        '''
        - image - Image as specified by PIL module
        - sides_code - a 12 character long string, divided into 4 groups of 3
                       consecutive characters, where each group represents a code
                       for one side of the image (north, east, south, west) starting
                       from left to right: 'aaa bbb ccc ddd'
        '''
        self.image = image
        self.sides_code = sides_code


    def __repr__(self) -> str:
        return f'<sides_code={self.sides_code}, image={self.image}>'


    def rotate_tile(self, rotations: int = 0, rotate_direction: str = 'left') -> None:
        '''
        Rotates @image(if tile has one) and shifts @sides_code.

        - rotations - number of rotations
        - rotate_direction - rotating direction, counter-clockwise(left) or clockwise(right)

        Valid direction values: left, right
        '''
        if rotate_direction not in ALLOWED_ROTATION_DIRECTIONS:
            raise ValueError(f'Invalid rotate_direction: {rotate_direction}')

        self.image = self._get_rotated_image(rotations, rotate_direction)
        self.sides_code = self._get_shifted_sides_code(rotations * 3, rotate_direction)


    def _get_rotated_image(self,
                            rotations: int = 0,
                            rotate_direction: str = 'left') -> None|Image.Image:
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
            rotated_image = self.image.rotate(rotation_angle, expand=True)

            return rotated_image

        return None


    def _get_shifted_sides_code(self, shifts = 0, shift_direction: str = 'left') -> str:
        '''
        Shifts one character. Shifts @sides_code with wrap-around
        (first character becomes last(left) and vice versa(right)).
        
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

        return self.image.size


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


    def match_sides_code(self,
                         other: 'Tile',
                         self_direction: Direction,
                         other_direction: Direction) -> bool:
        '''
        Checks if Tile@self and Tile@other match sides_code on given directions.

        If sides_code match, returns True.
        Otherwise, returns False.

        - other - tile whose sides_code are matched to self
        - other_direction - side Direction of Tile@other
        - self_direction - side Direction of Tile@self
        '''
        if isinstance(self_direction, Direction) is False:
            raise TypeError('self_direction must be of type \'Direction\'')

        if isinstance(other_direction, Direction) is False:
            raise TypeError('other_direction must be of type \'Direction\'')

        if self_direction.is_invalid():
            raise ValueError('Invalid direction: self_direction')

        if other_direction.is_invalid():
            raise ValueError('Invalid direction: other_direction')

        # get the correct 3-character group of codes corresponding to given Directions

        self_group = self.get_code_group(self_direction)
        other_group = other.get_code_group(other_direction)

        return self_group == other_group[::-1]


    def get_code_group(self, direction: Direction) -> str:
        '''
        Returns the correct 3 character group from sides_code based on the direction:
        - NORTH - index range of [0:2], first set of 3 character in sides_code
        - EAST - index range of [3:5], second set of 3 character in sides_code
        - SOUTH - index range of [6:8], third set of 3 character in sides_code
        - WEST - index range of [9:11], forth set of 3 character in sides_code

        + direction - direction from which, slice is calculated
        '''
        code_slice = direction.get_slice()
        return self.sides_code[code_slice]
