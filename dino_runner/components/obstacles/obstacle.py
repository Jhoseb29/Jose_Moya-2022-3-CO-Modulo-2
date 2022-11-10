import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH, BIRD

class Obstacle(Sprite):

    def __init__(self, image, obstacle_type):
        self.image = image
        self.obstacle_type = obstacle_type
        self.rect = self.image[self.obstacle_type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.index = 0
        

    def update(self, game_speed, obstacles):
        #!cambiar a una imagen u otra para que haga el movimiento de las alas con las dos imagenes
        self.animate()

        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def animate(self):
        if self.image == BIRD:
            if self.index >= 30:
                self.index = 0
            if self.index < 15:
                self.obstacle_type = 0
            else:
                self.obstacle_type = 1
            self.index += 1


    def draw(self, screen):
        screen.blit(self.image[self.obstacle_type], (self.rect.x, self.rect.y))