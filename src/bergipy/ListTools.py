import numpy as np


def hilbertizer(input_list):
    output_list = []
    none_appended = False

    input_list = list(input_list)

    if len(input_list) % 2 == 1:
        input_list.append(None)
        none_appended = True

    while len(input_list) > 0:
        len_input_list = len(input_list)

        first_half = input_list[:len_input_list // 2]
        second_half = input_list[len_input_list // 2:]

        if len(first_half) % 2 == 0:
            output_list.append(first_half.pop(0))
            output_list.append(second_half.pop(0))

        if len(first_half) % 2 == 1:
            output_list.append(first_half.pop(len(first_half) // 2))
            output_list.append(second_half.pop(len(first_half) // 2))

        input_list = first_half + second_half

    if none_appended: output_list.pop(-1)

    return output_list


def hilbertizer_new(input_array: np.ndarray):
    if not isinstance(input_array, np.ndarray):
        raise TypeError('Input must be Numpy array')

    array_shape = np.array(input_array.shape)
    array_dimensions = len(input_array.shape)

    n_bits_necessary = len(format(np.max(array_shape) - 1, 'b'))
    format_specifier = f'0{n_bits_necessary}b'

    for flattened_idx in range(2**n_bits_necessary * array_dimensions):
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