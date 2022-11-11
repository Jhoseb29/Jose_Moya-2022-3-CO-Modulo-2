import pygame

from dino_runner.utils.constants import SCREEN_WIDTH,SCREEN_HEIGHT

def draw_message(
    message,
    screen,
    font_color = (255, 255, 255),
    font_size = 30,
    pos_x_center = SCREEN_WIDTH // 2,
    pos_y_center = SCREEN_HEIGHT // 2,

):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, font_color)
    text_rect = text.get_rect()
    text_rect.center = (pos_x_center, pos_y_center)
    screen.blit(text, text_rect)