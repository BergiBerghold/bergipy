import numpy as np
import cv2


def dec2reg(dec_value):
    return str(hex(dec_value)[2:].zfill(4))


def array2png(array, filename):
    array = array.astype(np.uint16)
    cv2.imwrite(filename, array << 6)


def png2array(filename):
    return cv2.imread(filename, cv2.IMREAD_UNCHANGED) >> 6


def unpack_raw10(bytestream, rows=2464, columns=3280, chunks=820, throwaway_bits=28):
    '''
    Examples for different modes of the IMX219:

    Full frame (default):
        rows = 2464
        columns = 3280
        chunks = 820
        throwaway_bits = 28

    2x2 Binning:
        rows = 1232
        columns = 3280
        chunks = 820
        throwaway_bits = 28

    4x4 Binning:
        rows = 616
        columns = 3280
        chunks = 820
        throwaway_bits = 28

    1920x1080 Windowing:
        rows = 1088
        columns = 1920
        chunks = 480
        throwaway_bits = 0

    256x256 Windowing:
        rows = 256
        columns = 256
        chunks = 64
        throwaway_bits = 0

    128x128 Windowing:
        rows = 128
        columns = 128
        chunks = 32
        throwaway_bits = 0
    '''

    expected_size = rows * (chunks * 5 + throwaway_bits)
    bytestream = bytestream[:expected_size]

    data_array = np.frombuffer(bytestream, dtype=np.uint8)
    data_array = data_array.reshape((rows, chunks * 5 + throwaway_bits))

    if throwaway_bits: data_array = data_array[:, :-throwaway_bits]
    data_array = data_array.reshape((rows, chunks, 5))

    data_array = data_array.astype(np.uint16)
    data_array[:, :, :-1] = data_array[:, :, :-1] << 2

    data_array[:, :, 3] |= data_array[:, :, 4] & 3
    data_array[:, :, 2] |= (data_array[:, :, 4] >> 2) & 3
    data_array[:, :, 1] |= (data_array[:, :, 4] >> 4) & 3
    data_array[:, :, 0] |= (data_array[:, :, 4] >> 6)

    data_array = data_array[:, :, :4]
    data_array = data_array.reshape((rows, columns))

    return data_array
