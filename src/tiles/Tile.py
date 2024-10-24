from utils.Direction import Direction

class Tile:
    def __init__(self, image = None, rules = [-1, -1, -1, -1]):
        self.image = image
        self.rules = rules.copy()
    
    # rotates image counter-clockwise, and rules to the left
    def rotate_tile(self, rotations = 1):
        self.__rotate_image(rotations)
        self.__rotate_permissions(rotations)

    def __rotate_image(self, rotations = 1):
        if not self.image is None:
            self.image = self.image.rotate(90 * (rotations % 4))

    def __rotate_permissions(self, rotations = 1):
        if not self.image is None:
            self.rules = self.rules[rotations:] + self.rules[:rotations]

    def resize_image(self, size):
        self.image = self.image.resize((size, size))

    def rules_match(self, other, direction):
        if not isinstance(direction, Direction):
            direction = Direction[direction]
            
        if direction.is_valid() == True:
            return self.rules[direction.inverse()] == other.rules[direction]
        
if __name__ == '__main__':
    tile = Tile()
    tile.rotate_tile()