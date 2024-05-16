from dataclasses import dataclass

import numpy as np


@dataclass
class Line:
    angle: float
    shift: float

    # eq: shift = x cos(angle) + y sin(angle)
    # x = j - w // 2
    # y = h // 2 - i

    def points(self, h, w):
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
