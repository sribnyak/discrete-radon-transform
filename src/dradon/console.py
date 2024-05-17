"""Command line interface for dradon."""

import click
import cv2

from . import __version__
from . import dradon, draw_lines, get_lines_from_radon_image


@click.command()
@click.option("--radon_img", help="Save the radon image to file TEXT")
@click.option(
    "--lines_img", help="Save the original image with marked lines to file TEXT"
)
@click.argument("image")
@click.version_option(version=__version__)
def main(radon_img, lines_img, image):
    """Detect lines on IMAGE and print their parameters to standard output."""
    image_cv2 = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    radon_img_cv2, shift_step = dradon(image_cv2)
    if radon_img:
        cv2.imwrite(radon_img, radon_img_cv2 * 255)

    lines = get_lines_from_radon_image(radon_img_cv2, shift_step)
    for line in lines:
        click.echo(line)

    if lines_img:
        cv2.imwrite(lines_img, draw_lines(image_cv2, lines))
