"""Implementation of Discrete Radon Transform"""

from dataclasses import dataclass

import numpy as np


@dataclass
class Line:
    """A straight line on the plane.

    Attributes:
        angle: the angle between the normal vector and x axis, in radians
        shift: signed distance from the line to the origin

    Equation: shift = x cos(angle) + y sin(angle)

    When used for images of size (h, w), the following coordinates are used:
    1) x = j - w // 2
    2) y = h // 2 - i
    """

    angle: float
    shift: float

    def points(self, h, w):
        """Approximate the line with a set of pixel coordinates, yield them one by one.

        If the line's orientation is closer to horisontal, iterates over x axis
        and yields pixel (i, j) for each valid j.

        If the line's orientation is closer to vertical, iterates over y axis
        and yields pixel (i, j) for each valid i.

        Can be used to approximate an integral over the line with a sum,
        or for drawing the line.

        Args:
            h: Image height.
            w: Image width.

        Yields:
            Coordinates (i, j) of pixels.
        """

        if np.pi / 4 < self.angle < 3 * np.pi / 4:
            # iterate over x, compute y
            k = -1 / np.tan(self.angle)
            b = self.shift / np.sin(self.angle)
            for j in range(w):
                x = j - w // 2
                y = round(k * x + b)
                i = h // 2 - y
                if 0 <= i < h:
                    yield i, j
        else:
            # iterate over y, compute x
            k = -np.tan(self.angle)
            b = self.shift / np.cos(self.angle)
            for i in range(h):
                y = h // 2 - i
                x = round(k * y + b)
                j = x + w // 2
                if 0 <= j < w:
                    yield i, j


def dradon(image, out_shape=None):
    """Return a Discrete Radon Transform of an image.

    Calculates the Discrete Radon Transform of image.

    The result is an image `radon_image` of shape `(out_h, out_w)`,
    such that `radon_image[a, s]` is equal to the sum of pixels along the line
    `Line(a * angle_step, (s - out_w // 2) * shift_step)`, where
    `angle_step` and `shift_step` are the sampling intervals for angle and shift.

    Before returning, the resulted image is normalized to have values from 0 to 1.

    As `shift_step` cannot be calculated using only the result image,
    it is returned together with `radon_image`.

    Args:
        image: A one-channel image as a two-dimensinal numpy array.
        out_shape: tuple `(out_h, out_w)` - the shape of the output, or None.
            When set to None, the shape is defined automatically.
            Specifically, both `out_h` and `out_w` will equal the image's diagonal.

    Returns:
        radon_image: the Discrete Radon Transform of image.
        shift_step: the sampling interval for the line shift.

    Raises:
        TypeError: The function arguments are not instances of expected classes.
        ValueError: The input image is not 2-D or out_shape is not a tuple of 2 ints.
    """

    if not isinstance(image, np.ndarray):
        raise TypeError("image must be a numpy ndarray")
    if image.ndim != 2:
        raise ValueError("The input image must be 2-D")

    h, w = image.shape
    diag = np.sqrt(h * h + w * w)

    if out_shape is not None:
        if not isinstance(out_shape, tuple):
            raise TypeError("out_shape must be a tuple or None")
        if len(out_shape) != 2:
            raise ValueError("out_shape must be a tuple of 2 ints")

        out_h, out_w = out_shape

        if not isinstance(out_h, int) or not isinstance(out_w, int):
            raise ValueError("out_shape must be a tuple of 2 ints")

    else:  # if out_shape is None
        out_h = out_w = round(diag)
        out_shape = (out_h, out_w)

    radon_image = np.zeros(out_shape)

    angle_step = np.pi / out_h
    shift_step = diag / out_w
    # angle in [0, pi), shift in [-diag/2, diag/2]

    print("Calculating DRT: iteration", end=" ")
    for a in range(out_h):
        print(a, end=" ", flush=True)
        for s in range(out_w):
            line = Line(a * angle_step, (s - out_w // 2) * shift_step)
            radon_image[a, s] = 0
            for i, j in line.points(h, w):
                radon_image[a, s] += image[i, j]
    print("Done")

    # normalization for proper visualization
    max_val = radon_image.max()
    if max_val > 0:
        radon_image /= max_val

    return radon_image, shift_step


def get_lines_from_radon_image(radon_image, shift_step, threshold=0.8):
    """Return a list of lines, found on an image by Radon transform.

    If y is Discrete Radon Transform of image x, then bright pixels on y
    represent lines on x.

    This function takes y (together with shift_step, as returned by the dradon
    function) and returns the lines given by the pixels of y brighter than threshold.

    Args:
        radon_image: a 2-D array, the Discrete Radon Transform of an image.
        shift_step: the sampling interval for the line shift (see dradon function).
        threshold: a minimum value for a pixel of radon_image to be considered
            a line on the original image.

    Returns:
        A list of lines (instances of class Line).

    Raises:
        TypeError: radon_image is not a numpy ndarray.
        ValueError: radon_image is not 2-D.
    """
    if not isinstance(radon_image, np.ndarray):
        raise TypeError("radon_image must be a numpy ndarray")
    if radon_image.ndim != 2:
        raise ValueError("radon_image must be 2-D")

    lines = []

    h, w = radon_image.shape
    angle_step = np.pi / h
    for a in range(h):
        for s in range(w):
            if radon_image[a, s] >= threshold:
                lines.append(Line(a * angle_step, (s - w // 2) * shift_step))

    return lines


def draw_lines(image, lines):
    """Draw lines on a greyscale image

    Takes a greyscale image, and draws lines with red colour.

    Args:
        image: a greyscale image, as a 2-D numpy array.
        lines: a list of lines (instances of class Line).

    Returns:
        A 3-channel image with lines drawn on it.

    Raises:
        TypeError: image is not a numpy ndarray.
        ValueError: image is not 2-D.
    """

    if not isinstance(image, np.ndarray):
        raise TypeError("image must be a numpy ndarray")
    if image.ndim != 2:
        raise ValueError("The input image must be 2-D")

    h, w = image.shape
    marked_image = np.dstack([image] * 3)

    for line in lines:
        for i, j in line.points(h, w):
            marked_image[i, j] = [255, 0, 0]

    return marked_image
