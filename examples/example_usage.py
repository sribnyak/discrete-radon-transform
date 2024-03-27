import cv2
from dradon import dradon, get_lines_from_radon_image, draw_lines


image = cv2.imread('geometry_test.png', cv2.IMREAD_GRAYSCALE)
radon_image, shift_step = dradon(image)
cv2.imwrite('radon_transform.png', radon_image * 255)
lines = get_lines_from_radon_image(radon_image, shift_step)
cv2.imwrite('detected_lines.png', draw_lines(image, lines))
