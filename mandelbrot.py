###############################################################################
# Mandelbrot Set
# https://en.wikipedia.org/wiki/Mandelbrot_set
###############################################################################

import pygame

from colour import Color
from numba import jit
from time import perf_counter


TITLE = 'Mandelbrot Set'
WIDTH = 800
HEIGHT = 600
MAX_FRAME_RATE = 60
MAX_INTERATIONS = 100
BLUE = Color("BLUE")
WHITE = Color("WHITE")
BLACK = Color("BLACK")
R_W_COLOURS = list(BLUE.range_to(WHITE, int(MAX_INTERATIONS/2)))
W_B_COLOURS = list(WHITE.range_to(BLACK, int(MAX_INTERATIONS/2) + 1))
COLOURS = [c.hex_l for c in R_W_COLOURS] + [c.hex_l for c in W_B_COLOURS]


@jit(nopython=True)
def normalise(x, maxx, minx, a, b):
    '''
    Scale number x between a and b
    '''
    return (b - a) * ((x - minx) / (maxx - minx)) + a


@jit(nopython=True)
def colour(px: int, py: int) -> str:
    '''
    Return the escape iteration based upon the X,Y given normalised
    in to the mandelbrot set.
    '''
    x0 = normalise(px, 0, WIDTH, 0.47, -2.00)
    y0 = normalise(py, 0, HEIGHT, 1.12, -1.12)
    x = 0
    y = 0
    iter = 0
    while (x*x + y*y <= 2*2 and iter < MAX_INTERATIONS):
        xtemp = x*x - y*y + x0
        y = 2*x*y + y0
        x = xtemp
        iter += 1
    return iter


def mandelbrot(surface) -> None:
    '''
    Run through for Width/Height of the screen to visualise
    '''
    start = perf_counter()
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            surface.set_at((x, y), COLOURS[colour(x, y)])
    end = perf_counter()
    print("Elapsed time:", end - start)


def process_events() -> bool:
    '''
    Run through all events and perform actions on those that are important
    to us. Return True if we are still running, False otherwise.
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
    return True


def event_loop():
    '''
    Main event loop
    '''
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    mb_surface = pygame.Surface((WIDTH, HEIGHT))

    redraw = True

    while process_events():
        if redraw:
            mandelbrot(mb_surface)
            redraw = False
        screen.blit(mb_surface, (0, 0))
        pygame.display.update()
        clock.tick(MAX_FRAME_RATE)


if __name__ == '__main__':
    event_loop()
    exit()
