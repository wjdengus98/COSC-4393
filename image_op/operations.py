import math
from dip import *
"""
Do not import cv2, numpy and other third party libs
"""
class Operation:
    def init(self):
        pass

    def flip(self, image, direction="vertical"):
        """
        Perform image flipping along horizontal or vertical direction

        image: the input image to flip
        direction: direction along which to flip ("horizontal" or "vertical")

        return: output_image
        """
        if direction == "horizontal":
            output_image = image[:, ::-1]
        elif direction == "vertical":
            output_image = image[::-1, :]
        else:
            raise ValueError("Invalid direction. Choose 'horizontal' or 'vertical'.")

        return output_image

    @staticmethod
    def chroma_keying(foreground, background, target_color=(0, 200, 0), threshold=150):
        """
        Perform chroma keying to create an image where the targeted green pixels are replaced with
        the background.

        foreground: the input image with green background
        background: the input image with normal background
        target_color: the target color to be extracted (green) (default: (0, 200, 0))
        threshold: value to threshold the pixel proximity to the target color (default: 150)

        return: output_image
        """
        output_image = zeros(shape(foreground), dtype=uint8)

        for i in range(foreground.shape[0]):
            for j in range(foreground.shape[1]):
                pixel_color = foreground[i, j]
                distance = sqrt((pixel_color[0] - target_color[0]) ** 2 +
                                (pixel_color[1] - target_color[1]) ** 2 +
                                (pixel_color[2] - target_color[2]) ** 2)

                if distance < threshold:
                    output_image[i, j] = background[i, j]
                else:
                    output_image[i, j] = foreground[i, j]

        return output_image