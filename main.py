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


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)


def draw_win(win, birds, pipes, base, score, gen, pipe_ind):
    if gen == 0:
        gen = 1
    win.blit(BG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    for bird in birds:
        bird.draw(win)
    text = STAT_FONT.render('Score: ' + str(score), True, (255, 255, 255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render('Gen: ' + str(gen), True, (255, 255, 255))
    win.blit(text, (10, 10))
    pygame.display.update()


def main(genomes, config):
    global WIN, gen
    win = WIN
    gen += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:  # genome is tuple with id and object
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(g)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:  # no birds left, all 50 times done
            run = False
            break

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1  # more fitness for staying alive
            bird.move()

            output = nets[x].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:  # only 1 output neuron
                bird.jump()

        base.move()
        remove = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for collision
            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(WIDTH))

        for r in remove:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:  # if bird goes above or below window
                nets.pop(x)
                ge.pop(x)
                birds.pop(x)

        draw_win(WIN, birds, pipes, base, score, gen, pipe_ind)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction
                                , neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
