import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, SHIELD_TYPE

class ObstacleManager():
    def __init__(self):
        self.obstacles = []
        
    def update(self, game):
        if len(self.obstacles) == 0:
            obstacle_random = random.randint(0, 2)
            if obstacle_random == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS, 325))
            elif obstacle_random == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS, 300))
            elif obstacle_random == 2:
                self.obstacles.append(Bird(BIRD))
            
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                if game.player.type != SHIELD_TYPE:
                    game.death_count += 1
                    game.playing = False
                break
            else:
                self.obstacles.pop()
    

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset(self):
        self.obstacles = []



        

