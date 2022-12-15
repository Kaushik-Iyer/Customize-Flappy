import pygame
import neat
import time, os, random
from Bird import Bird
from Pipe import Pipe
from Base import Base
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
