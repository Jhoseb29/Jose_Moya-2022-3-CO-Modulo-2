import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, GAME_OVER

from dino_runner.components.dinosaur import Dinosaur 
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

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
        self.reset_obstacles()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def reset_obstacles(self):
        self.obstacle_manager.reset()
        self.score = 0
        self.game_speed = 20

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((0, 0, 0))
        self.draw_background()
        self.player.draw(self.screen) #! Dinausor class draw
        self.obstacle_manager.draw(self.screen)#! ObstacleManager class draw
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def text_menu(self, half_screen_width, half_screen_height):
            font = pygame.font.SysFont(FONT_STYLE, 30)
            text = font.render("Press any key to start", True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width + 250, half_screen_height - 250)
            self.screen.blit(text, text_rect)

    def image_game_over(self, half_screen_width,  half_screen_height):
            self.screen.blit(self.game_over_image, (half_screen_width + 150, half_screen_height -350))
            self.screen.blit(self.game_reset_image, self.replay_button)
            if self.replay_button.collidepoint(self.mouse_pos):
                pass

    def text_scores(self,half_screen_width, half_screen_height):
        font = pygame.font.SysFont(FONT_STYLE, 30)
        text = [font.render(f"Your Score: {self.score}", True, (255, 255, 255)),
        font.render(f"Your high score: {self.high_score}", True, (255, 255, 255)), 
        font.render(f"Your death count: {self.death_count}", True, (255, 255, 255))]
        index = 0
        for result in text:
                index += 30
                result_rect = result.get_rect()
                result_rect.center = (half_screen_width, half_screen_height)
                self.screen.blit(result, (result_rect.x + 250, result_rect.y -250  + index))

    def show_menu(self):
        self.screen.fill((0, 0, 0))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            self.text_menu(half_screen_height, half_screen_width)
        else:
            self.image_game_over(half_screen_height, half_screen_width)
            self.text_scores(half_screen_height, half_screen_width)
            

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
        text = font.render("Score: " + str(self.score), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

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

