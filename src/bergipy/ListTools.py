import numpy as np


def hilbertizer(input_array: np.ndarray):
    if not isinstance(input_array, np.ndarray):
        raise TypeError('Input must be Numpy array')

    array_shape = np.array(input_array.shape)
    array_dimensions = len(input_array.shape)

    n_bits_necessary = len(format(np.max(array_shape) - 1, 'b')) * array_dimensions
    format_specifier = f'0{n_bits_necessary}b'

    for flattened_idx in range(2**n_bits_necessary):
        binary = format(flattened_idx, format_specifier)
        reversed_binary = binary[::-1]

        array_indices = np.array([int(reversed_binary[offset::array_dimensions], 2) for offset in range(array_dimensions)])
        if (array_indices >= array_shape).any(): continue

        yield input_array[tuple(array_indices)]


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


def find_latest(array, value):
    array = np.asarray(array)
    array = array[array < value]
    idx = len(array) - 1
    return idx, array[-1]