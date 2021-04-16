import numpy as np
import pygame

from hyperparameters import goal, max_speed, screen_width, screen_height

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        self.end = False
        self.surf = pygame.Surface((screen_width//1.5, 20))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(screen_width-self.surf.get_width()//2,
                                               screen_height//1.5))
