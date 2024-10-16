from PIL import Image

from utils.Direction import convert_to_direction

class Tile:
    def __init__(self, image = Image.new('RGB', (40, 40)), side_permissions = [0, 0, 0, 0]):
        self.image = image
        self.side_permissions = side_permissions.copy()
    
    def rotate_permissions(self, rotations = 1):
        for r in range(rotations):
            temp = self.side_permissions[0]
            self.side_permissions[0] = self.side_permissions[1]
            self.side_permissions[1] = self.side_permissions[2]
            self.side_permissions[2] = self.side_permissions[3]
            self.side_permissions[3] = temp

    def match(self, other, direction):
        direction = convert_to_direction(direction)
        
        if direction.is_valid() == True:
            return self.side_permissions[direction.inverse().value] == other.side_permissions[direction.value]