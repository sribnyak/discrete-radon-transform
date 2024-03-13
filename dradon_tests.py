import numpy as np
import cv2
import random
from dradon import dradon, get_lines_from_radon_image, draw_lines

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


def test(image, true_lines, type):
    w, h = image.shape
    print(f"testing {type} lines...")
    radon_image, shift_step = dradon(image)
    lines = get_lines_from_radon_image(radon_image, shift_step)

    # cv2.imwrite(f'detected_{type}.png', draw_lines(image, lines))

    # проверяю совпадает ли множество true_lines и lines посредством поочередного включения, если совпадают, то значи
    # что алгоритм нашел все прямые и при этом не добавил ничего лишнего
    for true_line in true_lines:
        if not isin_true_line_lines(true_line, lines, h, w):
            print('test failed')
            for line in true_lines:
                print(line)  # вывожу пары точек задающих прямые, чтобы можно было понять, где ломается алгоритм
            return
    for line in lines:
        if not isin_line_true_lines(line, true_lines, h, w):
            print('test failed')
            for true_line in true_lines:
                print(true_line)  # вывожу пары точек задающих прямые, чтобы можно было понять, где ломается алгоритм
            return
    print("test passed")


num_lines = 5

if __name__ == "__main__":
    for i, image_size in enumerate([(30, 50), (40, 40), (50, 20), (50, 30)]):
        print(f"testing for image_size = {image_size}...")
        print("----------------------------------------------------------")

        horizontal_lines = lines(image_size, num_lines, "horizontal")
        selected_horizontal_lines = random.sample(horizontal_lines, random.randint(num_lines))
        image = create_image(image_size, selected_horizontal_lines)
        # cv2.imwrite(f'horizontal_{i}.png', image)
        test(image, selected_horizontal_lines, f"horizontal_{i}")

        print("----------------------------------------------------------")

        vertical_lines = lines(image_size, 5, "vertical")
        selected_vertical_lines = random.sample(vertical_lines, random.randint(num_lines))
        image = create_image(image_size, selected_vertical_lines)
        # cv2.imwrite(f'vertical_{i}.png', image)
        test(image, selected_vertical_lines, f"vertical_{i}")

        print("----------------------------------------------------------")

        diagonal_lines = lines(image_size, 5, "diagonal")
        selected_diagonal_lines = random.sample(diagonal_lines, random.randint(num_lines))
        image = create_image(image_size, selected_diagonal_lines)
        # cv2.imwrite(f'diagonal_{i}.png', image)
        test(image, selected_diagonal_lines, f"diagonal_{i}")

        print("----------------------------------------------------------")
