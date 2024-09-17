import numpy as np
import math

class Filtering:

    def __init__(self, image):
        self.image = image

    def get_gaussian_filter(self):
        """Initialzes/Computes and returns a 5X5 Gaussian filter"""
        sigma = 1.0
        filter_size = 5
        gaussian = np.zeros((filter_size, filter_size))
        center = filter_size // 2

        for i in range(filter_size):
            for j in range(filter_size):
                x = i - center
                y = j - center
                gaussian[i, j] = (1 / (2 * math.pi * sigma ** 2)) * math.e**(
                    - (x ** 2 + y ** 2) / (2 * sigma ** 2))

        gaussian /= np.sum(gaussian)

        return gaussian

        #return np.zeros((5, 5))

    def get_laplacian_filter(self):
        """Initialzes and returns a 3X3 Laplacian filter"""
        laplacian = np.array([[0, 1, 0],
                             [1, -4, 1],
                             [0, 1, 0]])

        return laplacian


        #return np.zeros((3, 3))

    def filter(self, filter_name):
        """Perform filtering on the image using the specified filter, and returns a filtered image
            takes as input:
            filter_name: a string, specifying the type of filter to use ["gaussian", laplacian"]
            return type: a 2d numpy array
                """
        if filter_name == "gaussian":
            gaussian_filter = self.get_gaussian_filter()
            pad_width = 2
            padded_shape = (self.image.shape[0] + 2 * pad_width, self.image.shape[1] + 2 * pad_width)
            padded_image = np.zeros(padded_shape, dtype=np.float32)
            padded_image[pad_width:-pad_width, pad_width:-pad_width] = self.image

            filtered_image = np.zeros_like(self.image, dtype=np.float32)

            for i in range(self.image.shape[0]):
                for j in range(self.image.shape[1]):
                    region = padded_image[i:i + 5, j:j + 5]
                    filtered_value = np.sum(region * gaussian_filter)
                    filtered_image[i, j] = filtered_value

        elif filter_name == "laplacian":
            laplacian_filter = self.get_laplacian_filter()
            pad_width = 1
            padded_shape = (self.image.shape[0] + 2 * pad_width, self.image.shape[1] + 2 * pad_width)
            padded_image = np.zeros(padded_shape, dtype=np.float32)
            padded_image[pad_width:-pad_width, pad_width:-pad_width] = self.image

            filtered_image = np.zeros_like(self.image, dtype=np.float32)

            for i in range(self.image.shape[0]):
                for j in range(self.image.shape[1]):
                    region = padded_image[i:i + 3, j:j + 3]
                    filtered_value = np.sum(region * laplacian_filter)
                    filtered_image[i, j] = max(filtered_value, 0)

        else:
            print("Invalid filter name")
            return self.image

        return filtered_image.astype(np.uint8)




        #return self.image

