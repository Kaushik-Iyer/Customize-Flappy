
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




class Base:
    VEL = 5
    WIDTH = BASE.get_width()
    IMG = BASE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
