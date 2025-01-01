from os import listdir

from PIL import Image


class ImageFileReader:
    def read(self, image_path, extension='.png'):
        files = [f for f in listdir(image_path) if f.endswith(extension)]
        images = {}

        for f in files:
            image = Image.open(f'{image_path}/{f}')
            images[f[:-4]] = image

        return images
    
    
    # def resize_all(self, size = 40):
    #     for f in self.files:
    #         image = self.images[f[:-4]]
    #         self.images[f[:-4]] = image.resize((size, size))