import numpy as np
import cv2


def get_subpixel(image, x, y):
    x -= 0.5
    y -= 0.5

    patch = cv2.getRectSubPix(image, (1,1), (x, y), np.zeros((1,1)), cv2.CV_32F)

    if patch is not None:
        return patch[0][0]

    return None


def grayscale_to_rgb(image):
    return np.stack((image,) * 3, axis=-1)