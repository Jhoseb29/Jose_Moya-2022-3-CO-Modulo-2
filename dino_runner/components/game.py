import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, GAME_OVER, DEFAULT_TYPE

from dino_runner.components.dinosaur import Dinosaur 
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.message import draw_message
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:
    def __init__(self):
        pygame.init()
        self.game_over_image = pygame.transform.scale(GAME_OVER[0], (200, 36))
        self.game_reset_image = pygame.transform.scale(GAME_OVER[1], (30, 36))
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.running = False
        self.score = 0
        self.death_count = 0
        self.high_score = 0
        self.mouse_pos = (-1, -1)
        self.replay_button = self.game_reset_image.get_rect()
        self.replay_button.x = SCREEN_WIDTH // 2 -18
        self.replay_button.y = SCREEN_HEIGHT // 2 - 50


    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.reset_all()
        
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def reset_all(self):
        self.power_up_manager.reset_power_ups()
        self.obstacle_manager.reset()
        self.playing = True
        self.game_speed = 20
        self.score = 0
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.update_score()
        
        


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((0, 0, 0))
        self.draw_background()
        self.player.draw(self.screen) #! Dinausor class draw
        self.obstacle_manager.draw(self.screen)#! ObstacleManager class draw
        self.power_up_manager.draw(self.screen) #! PowerUpManager class draw
        self.draw_power_up_time()
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    

    def image_game_over(self, half_screen_width,  half_screen_height):
            self.screen.blit(self.game_over_image, (half_screen_width + 150, half_screen_height -350))
            self.screen.blit(self.game_reset_image, self.replay_button)
            if self.replay_button.collidepoint(self.mouse_pos):
                pass


    def show_menu(self):
        self.screen.fill((0, 0, 0))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            draw_message("press any key to start ...", self.screen)
        else:
            self.image_game_over(half_screen_height, half_screen_width)
            draw_message("press any key to restart ...", self.screen)
            draw_message(f"Your Score: {self.score}",self.screen,pos_y_center = half_screen_height + 30)
            draw_message(f"Highest score: {self.high_score}",self.screen,pos_y_center = half_screen_height + 60)
            draw_message(f"total deaths: {self.death_count}",self.screen,pos_y_center = half_screen_height + 90)
            

        pygame.display.update()
        self.handle_events_on_menu()

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.run()

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pos = event.pos   

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = (-1, -1)
    
    def draw_score(self):
        font = pygame.font.SysFont(FONT_STYLE, 20)
        text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0:
                draw_message(f'{self.player.type} enable for {time_to_show} seconds', self.screen, font_color = "violet", font_size=18,pos_x_center=508,pos_y_center=50)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < 500:
            self.game_speed += 1
        
        if self.score > self.high_score:
            self.high_score = self.score  


    def increase_death_count(self):
        self.death_count += 1


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

