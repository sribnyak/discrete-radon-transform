import numpy as np


def dradon(image, out_shape=None):
    if not isinstance(image, np.ndarray):
        raise TypeError(f'image must be a numpy ndarray')
    if image.ndim != 2:
        raise ValueError(f'The input image must be 2-D')
    if not out_shape:
        out_shape = image.shape  # TODO: implement optimal choice
    return np.zeros(out_shape)  # TODO: implement


def get_lines_from_radon_image(radon_image):
    if not isinstance(radon_image, np.ndarray):
        raise TypeError(f'radon_image must be a numpy ndarray')
    if radon_image.ndim != 2:
        raise ValueError(f'radon_image must be 2-D')
    return []  # TODO: implement


def draw_lines(image, lines):
    if not isinstance(image, np.ndarray):
        raise TypeError(f'image must be a numpy ndarray')
    if image.ndim != 2:
        raise ValueError(f'The input image must be 2-D')
    return image  # TODO: implement
