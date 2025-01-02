import pygame

pygame.init()
from numba import njit
from math import sqrt, log
from time import time


@njit(fastmath=True)
def checkPoint(x, y, depth):
    z = c = x + 1j * y

    k = 0
    for k in range(depth):
        # z = z ** 2 + c
        # z = z ** 2 - z  AV: 5
        # z = z ** 3 + z ** 2 - c
        # z = z ** 4 - z
        # z = z ** 8 - z ** 4 + z ** 2 + z
        # z = z ** 4 - z ** 2 - c ** z * z ** c
        # z = (z + 1) ** 2
        # z = (z**c) ** 2  # !!!
        # z = (c**z) ** 2  # !!!
        # z = (z**c) ** 3  # Плавное усложнение предыдущего
        # z = (z**c) ** 20 #
        # z = z ** 4 - z ** 2 - c ** z * z ** c
        # z = z ** 4 - z ** 2 - c ** z * z ** (c**1/8)
        # z = z ** 8 - z ** 4 - z ** 2 - c ** z * z ** c
        # z = - z ** 4 + z ** 2 - c**z * z**c  # cool
        # z = z ** 37 - z ** 31 - c**z * z**c  # cool
        # z = z ** 4 - z ** 2 - (c ** z * z ** c) ** 2
        # z = z ** 4 - z ** 2 - (c ** z * z ** c) ** 1/2
        # z = z ** 4 - z ** 2 - (c ** z * z ** c) * c
        # z = z ** (-5) - z
        # z = z ** (-5.5) - z
        # z = z ** (-4) - z
        # z = z ** (-5 - 1/3) - z
        # z = z ** (-5 - 1/5) - z
        # z = z ** (-8-1/2) - z  # чем дальше тем больше итераций нужно для того чтобы картинка "загорелась"
        # уже тут необходимо 100к+ итераций
        # !!! до этого момента стояла проверка abs(z)>4, хотя должно было быть >2
        # z = z ** 8 - z ** 4 - z**2 - z
        # z = z ** 37 - z ** 31 - c ** z * z ** c
        # z = z ** 17 - z ** 19 - c ** z * z ** c
        # z = 19 * z ** 17 - 17 * z ** 19 - c ** z * z ** c
        # z = z ** 4 + c * (2 * z**2 + c + 1)  # Same as original, but 1 iteration skipped
        # z = z ** 4 - c * (2 * z**2 + c + 1)  # got from putting formula inside formula
        # then creating "conjugates". Paper was used in process
        # z = z ** 4 - c * (2 * z ** 2 - c - 1)  # interesting as previous
        # z = z ** 4 - c * (-2 * z ** 2 - c - 1)  # same as original (signs)

        # interesting properties. Have tiny separate sub-fractals. Formula from calculating further abstracting previous
        # z = z ** 8 + c ** 2 * (4 * z**2 + 1) + c * z**2 * (4 * z**4 + 2 * z**2 + 4)
        # z = z ** 8 - c ** 2 * (4 * z ** 2 + 1) + c * z ** 2 * (4 * z ** 4 + 2 * z ** 2 + 4)  # mirrored previous?
        # z = z ** 8 + c ** 2 * (4 * z ** 2 - 1) + c * z ** 2 * (4 * z ** 4 + 2 * z ** 2 + 4)  # why not
        # z = z ** 8 + c ** 2 * (4 * z ** 2 + 1) + c * z ** 2 * (4 * z ** 4 - 2 * z ** 2 - 4)  # cool

        # Now there are 3 lines of formulas and 2 new variables | Cool
        # a = z ** 8 + c ** 2 * (4 * z ** 2 - 1) + c * z ** 2 * (4 * z ** 4 + 2 * z ** 2 + 4)
        # b = z ** 4 + c * (2 * z**2 + c + 1)
        # z = b ** 4 + c * (2 * a**2 + c + 1)

        # Now there are 3 lines of formulas and 2 new variables | Cool, and have insanely tiny sub-fractals
        # a = z ** 8 + c ** 2 * (4 * z ** 2 - 1) + c * z ** 2 * (4 * z ** 4 + 2 * z ** 2 + 4)
        # b = z ** 4 + c * (2 * z ** 2 + c + 1)
        # z = b ** 4 - c * (2 * a ** 2 + c + 1)

        # Cool
        # a = z ** 8 - c ** 2 * (4 * z ** 2 - 1) + c * z ** 2 * (4 * z ** 4 + 2 * z ** 2 + 4)
        # b = z ** 4 - c * (2 * z ** 2 + c + 1)
        # z = b ** 4 - c * (2 * a ** 2 + c + 1)

        # Interesting
        # a = z ** 8 - c ** 2 * (4 * z ** 2 - 1) + c * z ** 2 * (4 * z ** 4 + 2 * z ** 2 + 4)
        # b = z ** 4 - c * (2 * z ** 2 + c - 1)
        # z = b ** 55 - c * (2 * a ** 2 + c - 1)

        # Interesting
        # a = z ** 8 - c ** 2 * (4 * z ** 2 + 1) + c * z ** 2 * (4 * z ** 4 + 2 * z ** 2 + 4)
        # b = z ** 4 - c * (2 * z ** 2 + c - 1)
        # z = b ** 2 - c * (2 * a ** 2 + c - 1)

        # z = (z ** 2 + c) ** 2 + c  # same as original, but have 1 less iteration
        # z = (z**2 + c) ** 2 - c  # interesting, and reminds some previous results
        # z = (z**2 - c) ** 2 - c  # mirrored original
        # z = (z ** 2 - c) ** 2 + c  # mirrored previous that remind something else

        # z = ((z ** 2 + c) ** 2 + c) ** 2 + c  # same as original, but have 2 less iterations
        # z = ((z ** 2 + c) ** 2 - c) ** 2 + c  # cool, in some way new
        # z = ((z ** 2 + c) ** 2 - c/2) ** 2 + c  # slightly and gently warped previous
        # z = ((z ** 3 + c) ** 3 + c) ** 2.5 + c  # smth in between z^2+c and z^3+c
        # z = ((z ** 3 + c) ** 3 + c) ** 3 + c  # same as z^3+c and have 2 less iterations

        # z = ((z ** 4 + c) ** 3 + c) ** 2 + c  # new way of warping between z^2+c, z^3+c and z^4+c simultaneously
        # z = ((z ** 4 - c) ** 3 - c) ** 2 + c
        # z = ((z ** 4 + c) ** 3 + c) ** 2 + z  # Wierd and interesting
        # z = ((z ** 4 + z) ** 3 + z) ** 2 + z  # as wierd as previous

        # z = ((z**14 - z) ** 3 - z) ** 2 + z
        # z = ((z**2 + c) ** 2 + c) ** 2 + c*z
        # z = ((z**2 + c) ** 2 + c) ** 2 + c**z
        # z = ((z ** 34 + c) ** 17 + c) ** (z*2) + c ** z  # weirdly, but this also interesting
        # z = ((z ** 34 + c**9) ** 17 + c) ** (z * 2) + c ** z  # just slightly warped previous
        # z = ((z ** 61 + c) ** 37 + c) ** (z * 31) + c ** z  # noticeably warped previous (origin with 34, 17, 2)
        # z = ((z ** 1 + c) ** 3 + c) ** (z * 7) + c ** z  # Interesting + have more than usual (bigger) size
        # z = (((z ** 11 + c) ** 3 + c) ** (z * 7) + c ** z) ** 2 + c  # Very interesting, slightly warped previous
        # z = (((z ** 3 + c) ** 11 + c) ** (z * 3) + c ** z) ** 7 + c  # Obviously warped previous + interesting

        # warped previous. Might remind dragon or goat silhouette
        # z = (((z ** 3 + c) ** (11**z) + c) ** (z * 3) + c ** z) ** 7 + c
        # z = (((z ** 3 + c) ** (11**z) + c) ** (z * 39) + c ** z) ** 7 + c  # less readable previous variant

        # Really chaotic, but have original mandelbrot set at
        # real: -0.5510537695737304
        # imag: -0.004315655639898554
        # zoom: 2^13.5
        # z = (((z ** 3 + c) ** (2**z) + c) ** (z * 3) + c ** z) ** 2 + c

        # optimized by claude 3.5, but I don't get how
        # z = ((3*z + c) * (2 ** z) + 3*z*c + c) ** 2 + c  # Interesting, have 2 equal and not mirrored mandelbrot sets
        # looks like just more copies of mandelbrot set along real axis. Not much warping and cute small "stars"

        # z = 2 ** z - z  # just 2 area with 1 iteration
        # z = 2 ** z + c  # cardioid with cuts
        # z = 3 ** z + c  # more warped cardioid and more cuts

        # --------------------------------------
        # z = 3 ** (z*c)  # Interesting. Seems infinite by axis, have diagonal asymptote
        # Have 3d effects at
        # real: 0.7812399310078381
        # imag: 0.5046522345510828
        # zoom: 2^9.5
        # fascinating overlapping of iso lines

        # z = 2 ** (z * c)  # Very interesting. Have features of previous, but even better

        # z = 2 ** (z**2)  # Even more interesting. More overlapping + 3D
        # z = 3 ** (z**3)  # variant of previous
        # z = 3 ** (z ** 2)  # ~boring
        # z = 2 ** (z**3)  # Interesting
        # z = 4 ** (z ** 4)  # boring, no new features, but continue previous

        # z = 4 ** (z**c)  # different kind of overlapping
        # z = 2 ** (z**c)  # more pure kind of previous

        # --------------------------------------
        # !!!! я всё это время забыл закомментировать формулу z = 3 ** (z*c) !!!!

        # !!! so formula actually was:
        # z = 2 ** (3 ** (z*c) ** c)  # but its works different

        # but this works:
        # z = 3 ** (z*c)
        # z = 2 ** (z ** c)

        # z = 2 ** ((3 ** (z*c)) ** c)  # Yeah, need parenthesis

        # z = 2 ** (z**2) # simpler, have 2 asymptote
        # z = 2 ** (z**c)  # interesting
        # z = 2 ** (z*c)  # define structure for 3d effects, have cute lines and overlapping "balls"

        if abs(z) > 2:
            break
    if k == depth - 1:
        k = -1

    return k

def chooseColor(n: int | None):
    if n is None:
        return 160, 200, 150
    color = [0, 0, 0]
    if n < 0:
        return color

    def quad(n):
        return sqrt(255 * 255 - n * n)

    if n > 4:
        k = log(n + 1, 1.0010)
    else:
        k = n * 20
    # k = (n**0.25)*250*1.3-130

    if 0 < k % 765 < 510:
        color[0] = quad(abs(255 - k % 765))
    if 255 < k % 765 < 765:
        color[1] = quad(abs(510 - k % 765))
    if 510 < k % 765 < 765:
        color[2] = quad(abs(765 - k % 765))
    if 0 <= k % 765 < 255 and k > 255:
        color[2] = quad(abs(0 - k % 765))

    return color


class Time:
    def __init__(self):
        self.last = time()

    def tick(self):
        if time() - self.last > 0.03:
            self.last = time()
            return True
        return False


class Info:
    x = 0
    y = 0
    scale = 1
    depth = 100
    surfaces = [0, 0, 0, 0]

    @property
    def zoom(self):
        return (2 ** self.scale) / 2

    @property
    def pix_offset(self):
        return (4 / self.zoom) / 384

    @property
    def left(self):
        return self.x - 192 * 3 * self.pix_offset

    @property
    def up(self):
        return self.y + 108 * 3 * self.pix_offset

    def move(self, x, y):
        if x > 0:
            self.x += 70 * self.pix_offset
        if x < 0:
            self.x -= 70 * self.pix_offset
        if y > 0:
            self.y += 70 * self.pix_offset
        if y < 0:
            self.y -= 70 * self.pix_offset
        self.littlesurface = False
        self.middlesurface = False
        self.normalsufrace = False

    def zooming(self, In):
        if In:
            self.scale += 0.5
        else:
            self.scale -= 0.5
        self.littlesurface = False
        self.middlesurface = False
        self.normalsufrace = False

    def changedepth(self, up):
        if up:
            self.depth *= 1.25
        else:
            self.depth /= 1.25
        self.depth = int(self.depth)
        self.littlesurface = False
        self.middlesurface = False
        self.normalsufrace = False

    def check_keys(self):
        changed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d,
                                 pygame.K_z, pygame.K_x, pygame.K_e, pygame.K_q,
                                 pygame.K_r):
                    changed = True
                if event.key == pygame.K_w:
                    self.move(0, 1)
                if event.key == pygame.K_s:
                    self.move(0, -1)
                if event.key == pygame.K_a:
                    self.move(-1, 0)
                if event.key == pygame.K_d:
                    self.move(1, 0)
                if event.key == pygame.K_z:
                    self.changedepth(False)
                if event.key == pygame.K_x:
                    self.changedepth(True)
                if event.key == pygame.K_e:
                    self.zooming(True)
                if event.key == pygame.K_q:
                    self.zooming(False)
                if event.key == pygame.K_r:
                    self.scale = 1
                    self.depth = 100
                    self.x = 0
                    self.y = 0
        if changed:
            print('real:', I.x)
            print('imag:', I.y)
            print(f'zoom: 2^{I.scale}', 'or', I.zoom, 'times')
            print('iterations limit:', I.depth)
            print(' -------------------------------------------- ')
            return True
        return False


def draw_surf(I, rel):
    for i in range(int(384 * 3 / rel)):
        points = []
        for j in range(int(216 * 3 / rel)):
            x = I.left + I.pix_offset * rel * i
            y = I.up - I.pix_offset * rel * j
            try:
                k = checkPoint(x, y, I.depth)
                color = chooseColor(k)
            except ZeroDivisionError:
                color = (160, 210, 150)
            except OverflowError:
                color = (150, 155, 210)
            points.append(color)
        yield points, i


def draw(I):
    for rel in 36, 24, 12, 4, 2, 1:
        for points, i in draw_surf(I, rel):
            for j, point in enumerate(points):
                pygame.draw.rect(sc, point, (i * rel, j * rel, rel, rel))
            yield


sc = pygame.display.set_mode((384 * 3, 216 * 3), pygame.HWSURFACE)
pygame.display.set_caption('Live view')

I = Info()
T = Time()
surface = pygame.Surface((384, 216))

run = True
while run:
    for _ in draw(I):
        if T.tick():
            pygame.display.update()
        if I.check_keys():
            break
    else:
        while True:
            if I.check_keys():
                break