import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING


class Dinosaur(Sprite):
    x_pos = 80
    y_pos = 310
    JUMP_SPEED = 6

    def __init__(self):
        self.image = RUNNING[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.step_index = 0
        self.dino_run = True
        self.jump_speed = self.JUMP_SPEED
        self.dino_jump = False
    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        
        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_run = True

        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.step_index += 1
    
    def jump(self):
        self.image = JUMPING
        self.rect.y -= self.jump_speed * 4

        self.jump_speed -= 0.5

        if self.jump_speed < -self.JUMP_SPEED:
            self.rect.y = self.y_pos
            self.dino_jump = False
            self.jump_speed = self.JUMP_SPEED

    

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))