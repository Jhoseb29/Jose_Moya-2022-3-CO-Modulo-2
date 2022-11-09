import random
import pygame
from dino_runner.components.obstacles.obstacle import Obstacle

from dino_runner.utils.constants import BIRD


class Bird(Obstacle):
    def __init__(self, image):
        self.obstacle_type = 0
        super().__init__(image, self.obstacle_type)
        self.rect.y = random.randint(75, 300)
        self.index = 0

   



        
    