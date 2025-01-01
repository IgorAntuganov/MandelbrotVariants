import pygame
import time
from dataclasses import dataclass
from typing import Generator

FRAME_TIME = .2  # in seconds

@dataclass
class MandelbrotConfig:
    rect_size: pygame.Rect = pygame.Rect((0, 0, 1024, 1024))
    coords_rect_left_top: tuple[float, float] = (-2, -2)
    coords_rect_size: tuple[float, float] = (4, 4)
    max_depth: int = 500


def get_pixel_size(config: MandelbrotConfig) -> tuple[float, float]:
    pixel_width = config.coords_rect_size[0] / config.rect_size.width
    pixel_height = config.coords_rect_size[1] / config.rect_size.height
    pixel_width = round(pixel_width, 15)
    pixel_height = round(pixel_height, 15)
    return pixel_width, pixel_height


def pixel_index_iterator(config: MandelbrotConfig) -> Generator[tuple[int, int], None, None]:
    for i in range(config.rect_size.width):
        for j in range(config.rect_size.height):
            yield i, j


def pixel_index_to_cords(config:     MandelbrotConfig,
                         ij_tuple:   tuple[int, int],
                         pixel_size: tuple[float, float]) -> tuple[float, float]:
    i, j = ij_tuple
    pixel_width, pixel_height = pixel_size

    left = config.coords_rect_left_top[0]
    top = config.coords_rect_left_top[1]
    x = left + pixel_width * i
    y = top + pixel_height * j

    if i == 0 and j == 0:
        print('first xy', x, y)
    if i == config.rect_size.width-1 and j == config.rect_size.height-1:
        print('last xy', x, y)
    return x, y


def mandelbrot_value(x: float, y: float, depth: int) -> int:
    z: complex
    c: complex
    z = c = x + 1j * y
    if z == 0:
        return depth
    for k in range(depth):
        # z = z ** 2 + c
        # Another variants:
        # z = z**3 + 3 * z**2 + c  # same as original, but smaller
        # z = z**4 + 4 * z**3 + 12 * z**2 + c   # same as original, but smaller
        # z = z ** 3 - 3 * z**2 + c  # same as original, but mirrored
        # z = z ** 3 + 1/27 * z**-2 + c
        # z = z ** 4 + 1/9 * z**-3 + c
        # z = z ** 3 + z ** 2 + z + c
        # z = z ** 2 + 1/1.41 * z + c
        # z = (z**2-c) ** 2 + c
        # z = (z - 1/9*c**3) ** 2 + c
        # z = - z ** 5 + z ** 4 - z ** 3 + z ** 2 - c
        # z = z.real ** 2 + 1j/20 * z.imag ** 3 + c
        # z = z ** 2 - z  # Почти то что нужно, но возрастающие итерации крайне компактны, плохо отображаются
        # Отображаются только диски, причем каждый диск "погружен"|"вминается" в месте контакта в большую фигуру

        # z = z ** 2 - z
        # z = z ** 3 + z кажется диагональным отражением и незначительным усложнением предыдущего
        # z = z ** 4 + z ** 2 + z  # Довольно любопытные варианты c 4мя вариантами расстановки знаков
        # z = z ** 4 - z ** 2 + z  # Довольно любопытные варианты
        # z = z ** 4 - z ** 2 - z  # Довольно любопытные варианты
        # z = z ** 4 + z ** 2 - z  # Довольно любопытные варианты

        # еще варианты, с минусом перед z**4
        # z = -z**4 + z**2 + z
        # z = -z ** 4 + z ** 2 - z
        # z = -z**4 - z**2 + z
        # z = -z**4 - z**2 - z

        # следующий шаг предыдущей последовательности:
        # z = z ** 8 + z ** 4 + z ** 2 + z
        # z = z ** 8 + z ** 4 + z ** 2 - z
        # z = z ** 8 + z ** 4 - z ** 2 + z
        # z = z ** 8 + z ** 4 - z ** 2 - z
        # z = z ** 8 - z ** 4 + z ** 2 + z
        # z = z ** 8 - z ** 4 + z ** 2 - z
        # z = z ** 8 - z ** 4 - z ** 2 + z
        # z = z ** 8 - z ** 4 - z ** 2 - z
        # Все результаты достойные, достаточно непрерывные для красоты
        # z = - z ** 8 + z ** 4 + z ** 2 + z

        # Дальнейшее усложнение:
        # z = z ** 32 + z ** 16 + z ** 8 - z ** 4 - z ** 2 - z
        # z = z ** 32 + z ** 16 + z ** 8 - z ** 4 - z ** 2 - z + c**z
        # z = z ** 32 + z ** 16 + z ** 8 - z ** 4 - z ** 2 - z + z**c
        # z = z ** 2 - z**c
        # z = z ** 2 + c ** z
        # z = z ** 2 + c**z + z**c
        # z = z ** 2 + c**z - z**c
        # z = z ** 2 - c ** z + z ** c
        # z = z ** 2 - c ** z - z ** c
        # z = z**4 + z ** 2 - c ** z - z ** c
        # z = z ** 4 - z ** 2 - c ** z - z ** c
        # z = z ** 4 - z ** 2 - c ** z * z ** c

        # z = (z + 1) ** 2  # Слегка искаженные песочные часы
        # z = (z - 1) ** 2  # Что то среднее. Похоже на некоторое множество жулиа
        # z = (z - c) ** 2  # Отраженное по вертикали множество мандельброта

        # z = (z**c) ** 2
        # Имеет крайне много элементов: складки, приятные эффекты пикселизации, баги отображения,
        # позволяет отдалять, есть ZeroDivisionError, OverflowError

        hypo_sqr = z.real ** 2 + z.imag ** 2
        if hypo_sqr > 4:
            return k
    return depth


def value_to_color(value: int | None, depth: int) -> tuple[int, int, int]:
    if value is None:
        return 160, 200, 150
    if value == depth:
        return 0, 0, 0
    value = 64 * (value/8) ** .5
    if value < 100:
        color_value = (100 - value) * 2
        return (int(color_value),) * 3
    else:
        color_value = abs(255 - depth % 510)
        return color_value, 0, 0

def update_screen(screen: pygame.Surface, image: pygame.Surface):
    screen.blit(image, (0, 0))
    pygame.display.flip()

def main(config: MandelbrotConfig):
    start = time.time()
    time_tick = time.time()
    screen = pygame.display.set_mode(config.rect_size.size)

    image = pygame.Surface(config.rect_size.size)
    pixel_size = get_pixel_size(config)
    for ij in pixel_index_iterator(config):
        x, y = pixel_index_to_cords(config, ij, pixel_size)
        try:
            value = mandelbrot_value(x, y, config.max_depth)
            color = value_to_color(value, config.max_depth)
        except ZeroDivisionError:
            color = (160, 210, 150)
        except OverflowError:
            color = (150, 155, 210)
        try:
            image.set_at(ij, color)
        except ValueError:
            print(color)

        if time.time() - time_tick > FRAME_TIME:
            [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
            update_screen(screen, image)
            time_tick = time.time()

    update_screen(screen, image)
    print('Elapsed time:', round(time.time()-start, 10))

    while True:
        [exit() for event in pygame.event.get() if event.type == pygame.QUIT]


if __name__ == '__main__':
    main(MandelbrotConfig())
