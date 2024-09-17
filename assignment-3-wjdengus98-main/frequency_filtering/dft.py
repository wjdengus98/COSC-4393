# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries
import dip

from dip import *
import math
import numpy as np

class Dft:
    def __init__(self):
        pass

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""

        N = len(matrix)
        fft_matrix = [[0 for _ in range(N)] for _ in range(N)]

        for u in range(N):
            for v in range(N):
                sum_complex = 0
                for i in range(N):
                    for j in range(N):
                        angle = (-2j * math.pi * (((u * i) / N) + ((v * j) / N)))
                        sum_complex += matrix[i][j] * math.e**angle
                fft_matrix[u][v] = sum_complex

        return fft_matrix

        #checking dft value
        # np.random.seed(42)
        # forward_fourier_transform = np.fft.fft2(matrix)
        # return forward_fourier_transform

        ##return matrix

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        You can implement the inverse transform formula with or without the normalizing factor.
        Both formulas are accepted.
        takes as input:
        matrix: a 2d matrix (DFT) usually complex
        returns a complex matrix representing the inverse fourier transform"""
        N = len(matrix)
        ift_matrix = [[0 for _ in range(N)] for _ in range(N)]

        for i in range(N):
            for j in range(N):
                sum_complex = 0
                for u in range(N):
                    for v in range(N):
                        angle = (2j * math.pi * (((u * i) / N) + ((v * j) / N)))
                        sum_complex += matrix[u][v] * math.e**angle
                ift_matrix[i][j] = sum_complex / (N * N) #Normalizing factor

        return ift_matrix

    def magnitude(self, matrix):
        """Computes the magnitude of the input matrix (iDFT)
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the complex matrix"""
        N = len(matrix)
        magnitude = [[0 for _ in range(N)] for _ in range(N)]

        for u in range(N):
            for v in range(N):
                magnitude[u][v] = math.sqrt(matrix[u][v].real ** 2 + matrix[u][v].imag ** 2)

        return magnitude
