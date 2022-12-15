import pygame
import neat
import time, os, random


pygame.font.init()
DRAW_LINES = False
WIDTH = 500
HEIGHT = 800
FLOOR = 730
gen = 0
BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.jpg'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.jpg'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.jpg')))]
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
BASE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
STAT_FONT = pygame.font.SysFont('comicsans', 50)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE, False, True)
        self.PIPE_BOTTOM = PIPE

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        bird_mask = bird.mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if t_point or b_point:
            return True
        return False