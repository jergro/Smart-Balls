import numpy as np
from ball import Ball
from hyperparameters import sample_size, brain_size

class Population:
    def __init__(self):
        self.balls = []
        self.fitnessSum = 0
        self.champion = 0
        self.gen = 0
        self.minStep = brain_size
        self.size = sample_size

    def populate(self):
        for i in range(self.size):
            self.balls.append(Ball())

    def calculate_fitness(self):
        for ball in self.balls:
            ball.calculate_fitness()

    def population_fitness(self):
        sigma = 0
        for ball in self.balls:
            sigma += ball.calculate_fitness()
        self.fitnessSum = sigma

    def update(self):
        for ball in self.balls:
            if ball.brain.step >= self.minStep:
                ball.isDead = True
            else:
                ball.update()

    def select_parent(self):
        self.population_fitness()
        fitpoint = self.fitnessSum*np.random.rand()
        sigma = 0
        for ball in self.balls:
            sigma += ball.fitness
            if sigma >= fitpoint:
                return ball
        return None

    def find_champ(self):
        m = 0
        champ = 0

        for i in range(self.size):
            self.balls[i].isBest = False
            if self.balls[i].fitness > m:
                m = self.balls[i].fitness
                champ = i

        self.champion = champ
        self.balls[champ].isBest = True

        if self.balls[champ].isGoal:
            self.minStep = self.balls[champ].brain.step

    def selection(self):
        # self.population_fitness()
        new_balls = [self.balls[self.champion].offspring()]  # best ball lives on.

        for i in range(1, self.size):
            parent = self.select_parent()
            child = parent.offspring()
            new_balls.append(child)

        self.balls = new_balls
        self.gen += 1

    def mutate(self):
        for i in range(self.size):
            self.balls[i].brain.mutate()

    def is_dead(self):
        for ball in self.balls:
            if not ball.isDead:
                return False
        return True
