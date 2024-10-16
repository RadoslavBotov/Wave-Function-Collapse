from os import listdir
from PIL import Image

class ImageLoader:
    def __init__(self, image_path = '', extension='.png'):
        self.image_path = image_path
        self.extension = extension
        self.files = []
        self.images = {}

    def load(self):
        self.files = [f for f in listdir(self.image_path) if f.endswith(self.extension)]

        for f in self.files:
            image = Image.open(f'{self.image_path}/{f}')
            self.images[f[:-4]] = image
    
    def resize_all(self, size = 40):
        for f in self.files:
            image = self.images[f[:-4]]
            self.images[f[:-4]] = image.resize((size, size))