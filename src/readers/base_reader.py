from abc import ABC, abstractmethod

from PIL import Image


class Reader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> dict[str, str|int|Image.Image]:
        pass