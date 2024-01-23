import numpy as np
import cv2


def get_subpixel(img, x, y):
    x -= 0.5
    y -= 0.5

    patch = cv2.getRectSubPix(img, (1,1), (x, y), np.zeros((1,1)), cv2.CV_32F)

    if patch is not None:
        return patch[0][0]

    return None