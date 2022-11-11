import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, RUNNING_SHIELD, JUMPING_SHIELD, DUCKING_SHIELD,DEFAULT_TYPE,SHIELD_TYPE

RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
JUM_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}


class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310

    Y_DUCK = 340
    JUMP_SPEED = 6


    def __init__(self):
        self.type = DEFAULT_TYPE
        #self.image = RUNNING[0]
        self.image = RUN_IMG[self.type][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.jump_speed = self.JUMP_SPEED
        self.dino_jump = False
        self.dino_duck = False
        self.has_power_up = False
        
    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        
        elif self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_run = True

        if user_input[pygame.K_DOWN]:
           self.dino_duck = True 
           self.dino_run = False
            
            
            

        if self.step_index >= 9:
            self.step_index = 0

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1
    
    def jump(self):
        self.image = JUM_IMG[self.type]
        self.rect.y -= self.jump_speed * 4

        self.jump_speed -= 0.5

        if self.jump_speed < -self.JUMP_SPEED:
            self.rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_speed = self.JUMP_SPEED

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_DUCK
        self.step_index += 1
    


    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))