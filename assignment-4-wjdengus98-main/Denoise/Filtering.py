import math
import numpy as np


class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        
        """

        self.image = image
        self.filterName = filter_name

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        
        # global_var: noise variance to be used in the Local noise reduction filter        
        self.global_var = var
        
        # S_max: Maximum allowed size of the window that is used in the adaptive median filter
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input ROI
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        
        return sum(roi) / (self.filter_size * self.filter_size)

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""

        product = 1
        num_pixel = len(roi)

        if num_pixel == 0:
            return 0 #Return to avoid division by 0 if roi is empty

        for i in roi:
            product *= i

        geometric_mean = product ** (1 / num_pixel)

        return geometric_mean

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""

        noise_var = self.global_var

        local_mean = math.fsum(roi) / len(roi)
        local_var = ((math.fsum(math.pow(i ,2) for i in roi) / len(roi)) - local_mean ** 2)

        center_pixel = roi[len(roi) // 2]

        local_noise = (center_pixel - (noise_var / local_var) * (center_pixel - local_mean))

        # for i in range(len(roi)):
        #     local_noise = (roi[i] - (noise_var / local_var) * (roi[i] - local_mean))
        return local_noise

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi
        Do not use any in-built median function from numpy or other libraries.
        """
        roi = np.array(roi)
        sorted_roi = np.sort(roi)
        length = len(sorted_roi)

        # If the length is odd, return the middle number
        if length % 2 == 1:
            return sorted_roi[length // 2]
        # If the length is even, return the average of the two middle numbers
        else:
            return (sorted_roi[length // 2 - 1] + sorted_roi[length // 2]) / 2
        
    def StageB(self, window, Zmin, Zmed, Zmax):

        x,y = window.shape

        Zxy = window[x // 2, y // 2]
        B1 = Zxy - Zmin
        B2 = Zxy - Zmax

        if B1 > 0 and B2 < 0:
            return Zxy
        else:
            return Zmed

    def get_adaptive_median(self, img, x, y, size, sMax):
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """
        baseWindow = size // 2
        filterWindow = img[x - baseWindow:x + baseWindow + 1, y - baseWindow:y + baseWindow + 1]

        # gets window intensity values
        Zmin = np.min(filterWindow)
        Zmed = self.get_median(filterWindow)
        Zmax = np.max(filterWindow)

        # Stage A
        A1 = Zmed - Zmin
        A2 = Zmed - Zmax

        if A1 > 0 and A2 < 0:
            return Filtering.StageB(self, filterWindow, Zmin, Zmed, Zmax)
        else:
            size += 2
            if size <= sMax:
                return Filtering.get_adaptive_median(self, img, x, y, size, sMax)
            else:
                return Zmed

    def filtering(self):
        """performs filtering on an image containing Gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernel and apply a mathematical
        operation for all the elements within the kernel. For example, mean, median, etc.

        Steps:
        1. add the necessary zero padding to the noisy image, that way we have sufficient values to perform the operations on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and for every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the output image.
        5. return the output image

        Note: You can create extra functions as needed. For example, if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        ImagewithNoise = self.image

        if self.filterName == 'adaptive_median':
            padValue = self.S_max // 2
            paddedImage = np.zeros((ImagewithNoise.shape[0] + 2 * padValue, ImagewithNoise.shape[1] + 2 * padValue))
            paddedImage[padValue:-padValue, padValue:-padValue] = ImagewithNoise
        else:
            padValue = self.filter_size // 2
            paddedImage = np.zeros((ImagewithNoise.shape[0] + 2 * padValue, ImagewithNoise.shape[1] + 2 * padValue))
            paddedImage[padValue:-padValue, padValue:-padValue] = ImagewithNoise

        outputImage = np.zeros(paddedImage.shape)

        if self.filterName == 'adaptive_median':
            for i in range(padValue, ImagewithNoise.shape[0] + padValue + 1):
                for j in range(padValue, ImagewithNoise.shape[1] + padValue + 1):
                    denoisedValue = Filtering.get_adaptive_median(self, paddedImage, i, j, self.filter_size, self.S_max)
                    outputImage[i, j] = denoisedValue


        elif self.filterName == 'arithmetic_mean':
            for i in range(padValue, ImagewithNoise.shape[0] + padValue + 1):
                for j in range(padValue, ImagewithNoise.shape[1] + padValue + 1):
                    windowFilter = paddedImage[i - padValue:i + padValue + 1, j - padValue:j + padValue + 1]
                    roiFilter = windowFilter.flatten()
                    denoisedValue = Filtering.get_arithmetic_mean(self, roiFilter)
                    outputImage[i, j] = denoisedValue

        elif self.filterName == 'geometric_mean':
            for i in range(padValue, ImagewithNoise.shape[0] + padValue + 1):
                for j in range(padValue, ImagewithNoise.shape[1] + padValue + 1):
                    windowFilter = paddedImage[i - padValue:i + padValue + 1, j - padValue:j + padValue + 1]
                    roiFilter = windowFilter.flatten()
                    denoisedValue = Filtering.get_geometric_mean(self, roiFilter)
                    outputImage[i, j] = denoisedValue

        elif self.filterName == 'local_noise':
            for i in range(padValue, ImagewithNoise.shape[0] + padValue + 1):
                for j in range(padValue, ImagewithNoise.shape[1] + padValue + 1):
                    windowFilter = paddedImage[i - padValue:i + padValue + 1,
                                   j - padValue:j + padValue + 1]  # gets window
                    roiFilter = windowFilter.flatten()  # flattens 2d image array to 1d array
                    denoisedValue = Filtering.get_local_noise(self, roiFilter)
                    outputImage[i, j] = denoisedValue

        elif self.filterName == 'median':
            for i in range(padValue, ImagewithNoise.shape[0] + padValue + 1):
                for j in range(padValue, ImagewithNoise.shape[1] + padValue + 1):
                    windowFilter = paddedImage[i - padValue:i + padValue + 1, j - padValue:j + padValue + 1]
                    roiFilter = windowFilter.flatten()
                    denoisedValue = Filtering.get_median(self, roiFilter)
                    outputImage[i, j] = denoisedValue

        return outputImage[padValue:-padValue, padValue:-padValue]  # crops image to remove padding

