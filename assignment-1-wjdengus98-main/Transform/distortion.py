from .interpolation import interpolation
from dip import *
import math

class Distort:
    def __init__(self):
        pass

    def distortion(self, image, k):
        """Applies distortion to the image
        image: input image
        k: distortion Parameter
        return the distorted image"""

        # Get center coordinates of the image
        center_x = int(image.shape[1] / 2)
        center_y = int(image.shape[0] / 2)

        # Create an empty matrix with the same shape as the input image
        distorted_image = image.copy()
        distorted_image[:, :] = 0  # Create a black image

        # Apply distortion to each pixel in the input image
        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                modX = (x - center_x)
                modY = (y - center_y)
                r = math.sqrt(modX ** 2 + modY ** 2)

                # Calculate distorted coordinates
                distorted_x = int(modX * (1 / (1 + k * r)))
                distorted_y = int(modY * (1 / (1 + k * r)))

                # Adjust distorted coordinates to the center of the image
                distorted_x += center_x
                distorted_y += center_y

                # Assign pixel value from the original image to the distorted image
                if 0 <= distorted_y < image.shape[0] and 0 <= distorted_x < image.shape[1]:
                    distorted_image[distorted_y, distorted_x] = image[ y,x]

        return distorted_image

    def correction_naive(self, distorted_image, k):
        """Applies correction to a distorted image by applying the inverse of the distortion function
        distorted_image: the distorted image
        k: distortion parameter
        return the corrected image"""

        # Get center coordinates of the distorted image
        x_center = int(distorted_image.shape[1] / 2)
        y_center = int(distorted_image.shape[0] / 2)

        # Initialize a zeros matrix for the corrected image with the same dimensions as the distorted image
        correc_naive_image = distorted_image.copy()
        correc_naive_image[:, :] = 0

        # Apply correction to each pixel in the distorted image
        for i in range(distorted_image.shape[1]):
            for j in range(distorted_image.shape[0]):
                # Apply a change in coordinate system to find point (i_c, j_c) with respect to center C
                i_c = i - x_center
                j_c = j - y_center

                # Apply the inverse distortion function to get (i_cd, j_cd)
                r = math.sqrt(i_c ** 2 + j_c ** 2)
                i_cd = int((1 + k * r) * i_c)
                j_cd = int((1 + k * r) * j_c)

                # Apply a change in the coordinate system again to get (i_d, j_d)
                i_d = i_cd + x_center
                j_d = j_cd + y_center

                # Copy pixel values from the distorted image to the corrected image
                if 0 <= i_d < distorted_image.shape[1] and 0 <= j_d < distorted_image.shape[0]:
                    correc_naive_image[j_d, i_d] = distorted_image[j, i]

        return correc_naive_image

    def correction(self, distorted_image, k, interpolation_type):
        """Applies correction to a distorted image and performs interpolation
        image: the input image
        k: distortion parameter
        interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
        return the corrected image"""
        x_c = int(distorted_image.shape[1] / 2)
        y_c = int(distorted_image.shape[0] / 2)

        # Create an empty matrix with the same shape as the input image
        correction_image = distorted_image.copy()
        correction_image[:, :] = 0 #

        for i in range(distorted_image.shape[1]):
            for j in range(distorted_image.shape[0]):
                i_c = (i - x_c)
                j_c = (j - y_c)
                r = math.sqrt(i_c ** 2 + j_c ** 2)

                # Calculate distorted coordinates
                i_cd = (i_c * (1 / (1 + k * r)))
                j_cd = (j_c * (1 / (1 + k * r)))

                # Adjust distorted coordinates to the center of the image
                i_d = i_cd + x_c
                j_d = j_cd + y_c

                if interpolation_type == "nearest_neighbor":
                    i_nn = round(i_d)
                    j_nn = round(j_d)
                    correction_image[j,i] = distorted_image[j_nn,i_nn]

                elif interpolation_type == "bilinear":
                    p1 = [math.floor(j_d), math.floor(i_d)] ##(x,y)
                    p2 = [math.floor(j_d), math.floor(i_d) + 1] ##(X,Y+1)
                    p3 = [math.floor(j_d) + 1, math.floor(i_d)] ## (x+1,y)
                    p4 = [math.floor(j_d) + 1, math.floor(i_d) + 1] ##(x+1,y+1)
                    biliner_func = interpolation()
                    result = biliner_func.bilinear_interpolation(i_d, j_d, p1, p2, p3, p4,
                                        distorted_image[p1[0], p1[1]], distorted_image[p2[0], p2[1]],
                                        distorted_image[p3[0], p3[1]], distorted_image[p4[0], p4[1]])

                    correction_image[j, i] = result
        return correction_image





