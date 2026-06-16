import numpy as np


def gauss_2d(input_array, x0, y0, sigma_x, sigma_y):
    x, y = np.indices(input_array.shape)

    input_array += np.exp(-( (x - x0)**2 / (2 * sigma_x**2) + (y - y0)**2 / (2 * sigma_y**2)))

    return input_array


def err_of_avrg(array):
    return np.nanstd(array) / np.sqrt(len(array))
