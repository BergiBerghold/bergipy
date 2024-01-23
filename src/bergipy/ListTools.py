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


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


def find_latest(array, value):
    array = np.asarray(array)
    array = array[array < value]
    idx = len(array) - 1
    return idx, array[-1]