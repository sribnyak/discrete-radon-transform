import numpy as np
import cv2
import random
from dradon import dradon, get_lines_from_radon_image

import pytest

# random.seed(42)


# создает изображение заданного размера с белыми линиями на черном фоне
def create_image(image_size, lines):
    image = np.zeros((image_size[1], image_size[0]), dtype=np.uint8)
    for line in lines:
        pt1, pt2 = line
        cv2.line(image, pt1, pt2, (255,), 1)
    return image


def get_points(line, h, w):
    points = set()
    for i, j in line.points(w, h):
        points.add((j, i))  # тут какой-то ужас, я так и не разобрался, но вроде работает (где-то первая координата
        # это ширина, вторая высота, где-то наоборот, методом проб и ошибок это работает
    return points


def are_similar_points(point1, point2):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]

    return max(abs(x1 - x2), abs(y1 - y2)) <= 3  # я решил что это достаточно логичное требование на близость точек


# Проверяю, лежит ли точка в списке точек
def is_in_points(point1, points):
    for point2 in points:
        if are_similar_points(point1, point2):
            return True
    return False


# Проверяем линии на "похожесть" т.к. обычную линию мы задаем парой точек, а с line из преобразования радона
# я не стал разбираться как она задается, я просто смотрю, лежат ли точки из true_line примерно там же, где и line
def are_similar_lines(true_line, line, h, w):
    points = get_points(line, h, w)
    for point in true_line:
        if not is_in_points(point, points):
            return False
    return True


# true_line и line совершенно по-разному заданные прямые, поэтому я пытаюсь понять лежит ли true_line где-то среди
# lines таким непонятным образом
def isin_true_line_lines(true_line, lines, h, w):
    for line in lines:
        if are_similar_lines(true_line, line, h, w):
            return True
    return False


# true_line и line совершенно по-разному заданные прямые, поэтому я пытаюсь понять лежит ли line где-то среди
# true_lines таким непонятным образом
def isin_line_true_lines(line, true_lines, h, w):
    for true_line in true_lines:
        if are_similar_lines(true_line, line, h, w):
            return True
    return False


# функция для генерации линий для будущих изображений
def lines(image_size, num_lines, type):
    lines = []

    if type == "horizontal":
        y_step = image_size[1] // (num_lines + 1)

        for i in range(1, num_lines + 1):
            y = i * y_step
            lines.append(((0, y), (image_size[0], y)))

    if type == "vertical":
        x_step = image_size[0] // (num_lines + 1)

        for i in range(1, num_lines + 1):
            x = i * x_step
            lines.append(((x, 0), (x, image_size[1])))

    if type == "diagonal":
        for i in range(num_lines):
            h0 = random.randint(0, image_size[0])
            w0 = 0

            h1 = random.randint(0, image_size[0])
            w1 = image_size[1]

            lines.append(((w0, h0), (w1, h1)))

    return lines


def run_test(image, true_lines):
    w, h = image.shape
    radon_image, shift_step = dradon(image)
    lines = get_lines_from_radon_image(radon_image, shift_step)

    # проверяю совпадает ли множество true_lines и lines посредством поочередного включения, если совпадают, то значи
    # что алгоритм нашел все прямые и при этом не добавил ничего лишнего
    assert all([isin_true_line_lines(true_line, lines, h, w) for true_line in true_lines])
    assert all([isin_line_true_lines(line, true_lines, h, w) for line in lines])


num_lines = 5
image_sizes = [(30, 50), (40, 40), (50, 20), (50, 30)]


@pytest.mark.parametrize("image_size", image_sizes)
def test_dradon_horizontal(image_size):
    horizontal_lines = lines(image_size, num_lines, "horizontal")
    selected_horizontal_lines = random.sample(horizontal_lines, random.randrange(num_lines))
    image = create_image(image_size, selected_horizontal_lines)
    run_test(image, selected_horizontal_lines)


@pytest.mark.parametrize("image_size", image_sizes)
def test_dradon_vertical(image_size):
    vertical_lines = lines(image_size, 5, "vertical")
    selected_vertical_lines = random.sample(vertical_lines, random.randrange(num_lines))
    image = create_image(image_size, selected_vertical_lines)
    run_test(image, selected_vertical_lines)


@pytest.mark.parametrize("image_size", image_sizes)
def test_dradon_diagonal(image_size):
    diagonal_lines = lines(image_size, 5, "diagonal")
    selected_diagonal_lines = random.sample(diagonal_lines, random.randrange(num_lines))
    image = create_image(image_size, selected_diagonal_lines)
    run_test(image, selected_diagonal_lines)
