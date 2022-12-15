import pygame
import neat
import time, os, random
# from Bird import Bird

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


class Bird:
    IMGS = BIRD
    ROTATION = 25
    VELOCITY = 20
    TIME = 5

    def __init__(self, x, y):
        self.vel = 0
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]


    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * (self.tick_count) + 0.5 * (3) * (self.tick_count) ** 2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y += d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.ROTATION:
                self.tilt = self.ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.VELOCITY

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.TIME * 2

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def mask(self):
        return pygame.mask.from_surface(self.img)

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)