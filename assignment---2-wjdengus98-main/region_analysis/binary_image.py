class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """ Computes the histogram of the input image
        takes as input:
        image: a greyscale image
        returns a histogram as a list """

        # iterate every pixel and we have to incremental each location of index
        hist = [0]*256

        # Iterate over each pixel in the image
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                # Increment the histogram bin which corresponds to the pixel value
                hist[image[i, j]] += 1

        return hist



    def find_threshold(self, hist):
        """ analyses a histogram to find the optimal threshold assuming that the input histogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value
        Note: Use the iterative method to calculate the histogram. Do not use the Otsu's method
        Write your code to compute the optimal threshold method.
        This should be implemented using the iterative algorithm discussed in class (See Week 4, Lecture 7, slide 40
        on teams). Do not implement the Otsu's thresholding method. No points are awarded for Otsu's method.
        """
        k = len(hist)
        t = k // 2 #-->int
        threshold = 0

        while True:
            # Compute μ1
            expected_val_1 = 0
            total_count = 0
            for i in range(t):
                expected_val_1 += hist[i] * i
                total_count += hist[i]
            mu1 = expected_val_1 / total_count if total_count > 0 else 0

            # Compute μ2
            expected_val_2 = 0
            total_count_2 = 0
            for i in range(t,k):
                expected_val_2 += hist[i] * i
                total_count_2 += hist[i]
            mu2 = expected_val_2 / total_count_2 if total_count_2 > 0 else 0

            new_threshold = round((mu1 + mu2) / 2)

            if new_threshold == threshold:
                break

            threshold = new_threshold

        return threshold

    def binarize(self, image, threshold):
        """ Comptues the binary image of the input image based on histogram analysis and thresholding
        takes as input
        image: a greyscale image
        threshold: to binarize the greyscale image
        returns: a binary image """

        bin_img = image.copy()

        for i in range(bin_img.shape[0]):
            for j in range(bin_img.shape[1]):
                if bin_img[i, j] > threshold:
                    bin_img[i, j] = 255
                else:
                    bin_img[i, j] = 0

        return bin_img


