from dip import *

class Rle:
    def __init__(self):
        pass

    def encode_image(self, binary_image):
        """
            Compress the image using RLE.
            """
        rows, cols = binary_image.shape  # Use rows and cols
        rle_code = []

        for i in range(rows):  # Iterate over each row
            current_pixel = binary_image[i, 0]
            c = 1
            for pixel in binary_image[i, 1:]:  # Iterate over the rest of the pixels in the row
                if pixel == current_pixel:
                    c += 1
                else:
                    rle_code.extend([current_pixel, c])
                    current_pixel = pixel
                    c = 1
            rle_code.extend([current_pixel, c])  # add the last run of the row

        return rle_code

    def decode_image(self, rle_code, height, width):
        """
            Decode RLE to get the original image.
            """
        decoded_image = zeros(height * width, dtype=uint8)
        idx = 0
        for i in range(0, len(rle_code), 2):
            val = rle_code[i]
            length = rle_code[i + 1]
            decoded_image[idx:idx + length] = val
            idx += length

        return decoded_image.reshape((height, width))







        




