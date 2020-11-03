import pygame
import pygame.locals as pygl
import numpy as np
from population import Population
from ball import Ball
from obstacle import Obstacle
from hyperparameters import *

pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Balls")
clock = pygame.time.Clock()

population = Population()
population.populate()

for ball in population.balls:
    ball.brain.randomize()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygl.KEYDOWN:
            if event.key == pygl.K_ESCAPE:
                running = False
        elif event.type == pygl.QUIT:
            running = False

    # black background
    screen.fill([0, 0, 0])

    # Goal
    pygame.draw.circle(screen, [255, 0, 0], goal, 10)

    # obstacle
    wall = Obstacle()
    short_wall = Obstacle()
    short_wall.rect.center = (screen_width-short_wall.surf.get_width(), screen_height//3)

    population.update()
    population.calculate_fitness()
    population.find_champ()

    for ball in population.balls:
        if pygame.sprite.collide_rect(wall, ball) or pygame.sprite.collide_rect(short_wall, ball):
            ball.isDead = True

        if not ball.isBest:
            # draws white ball
            pygame.draw.circle(screen, [255, 255, 255], np.rint(ball.pos).astype(int), 5)
        else:
            # draws green ball
            pygame.draw.circle(screen, [0, 255, 0], np.rint(ball.pos).astype(int), 8)
            fit_txt = ball.fitness

    # Here is the evolution
    if population.is_dead():
        population.selection()
        population.mutate()

    generation_text = pygame.font.SysFont('Consolas', 16).render('Generation: ' + str(population.gen),
                                                                 True,
                                                                 pygame.color.Color('White'))

    best_fitness_text = pygame.font.SysFont('Consolas', 16).render('Population fitness: ' + str(population.fitnessSum), True,
                                                                   pygame.color.Color('White'))

    min_step_text = pygame.font.SysFont('Consolas', 16).render('Minimum steps to goal: ' + str(population.minStep), True,
                                                               pygame.color.Color('White'))

    clock.tick(100)
    screen.blit(generation_text, (50, 50))
    screen.blit(best_fitness_text, (50, 70))
    screen.blit(min_step_text, (50, 90))
    screen.blit(wall.surf, wall.rect)
    screen.blit(short_wall.surf, short_wall.rect)
    pygame.display.flip()
pygame.quit()
