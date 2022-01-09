from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def color(r, g, b) -> np.array:
    return np.array([r, g, b])


class Bitmap:
    """
    Wrapper around pillow image and numpy array
    """

    def __init__(self, x, y):
        self.image = np.array(Image.new("RGB", (y, x)))

    def __getitem__(self, key):
        return self.image.__getitem__(key)

    def __setitem__(self, key, value):
        return self.image.__setitem__(key, value)

    def save(self, output_file):
        im = Image.fromarray((self.image))
        im.save(output_file)
        plt.imshow(self.image)
        plt.show()
