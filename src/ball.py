import numpy as np
import pygame
from brain import Brain
from hyperparameters import goal, max_speed, screen_width, screen_height

class Ball(pygame.sprite.Sprite):
    """
    Class to keep track of a ball's location and gradient.
    It keeps track of fitness, if the goal is reached, if its dead
    or if its the best one in the population.
    """
    def __init__(self):
        super(Ball, self).__init__()
        self.pos = np.array([screen_width//2, screen_height])
        self.vel = np.array([0, 0])
        self.acc = np.array([0, 0])
        self.maxSpeed = max_speed
        self.fitness = 0
        self.surf = pygame.Surface((2, 2))
        self.rect = self.surf.get_rect(center=self.pos)

        self.isBest = False
        self.isDead = False
        self.isGoal = False

        self.brain = Brain()

    def update(self):
        if not self.isDead:
            self.move()
            if self.pos[0] <= 0 or self.pos[0] >= screen_width or self.pos[1] <= 0 or self.pos[1] >= screen_height:
                self.isDead = True
            if ((self.pos[0]-goal[0])**2 + (self.pos[1]-goal[1])**2)**0.5 < 10:
                self.isGoal = True
                self.isDead = True

            self.rect.center = self.pos
            self.brain.step += 1

    def move(self):
        self.acc = np.array([np.cos(self.brain.directions[self.brain.step]),
                             np.sin(self.brain.directions[self.brain.step])])
        self.vel = self.vel + self.acc
        self.pos = self.pos + self.vel + 0.5 * self.acc

        if self.vel[0] ** 2 + self.vel[1] ** 2 > self.maxSpeed:
            # max speed * direction
            self.vel = self.maxSpeed * self.vel / (self.vel[0] ** 2 + self.vel[1] ** 2)

    def offspring(self):
        child = Ball()
        child.brain.directions = self.brain.directions
        return child

    def calculate_fitness(self):
        if self.isGoal:
            fitness = 1/16 + 1000 / (self.brain.step**2)
        else:
            fitness = 1 / ((self.pos[0] - goal[0]) ** 2 + (self.pos[1] - goal[1]) ** 2)**0.5
        self.fitness = fitness
        return fitness
