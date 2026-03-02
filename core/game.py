import pygame
import os
import random
import settings

from core.game_state import GameState
from entities.snake import Snake
from managers.spawn_manager import SpawnManager
from managers.score_manager import ScoreManager
from managers.sound_manager import SoundManager


class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("HungrySnake")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 30)

        self.state = GameState.MENU
        self.running = True

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.spawn_manager = SpawnManager(
            settings.WIDTH,
            settings.HEIGHT,
            settings.SNAKE_SIZE
        )

        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager(BASE_DIR)

        self.load_assets()

        self.snake = None
        self.apple_positions = []
        self.pear_positions = []
        self.obstacles = []
        self.fps = settings.START_FPS

        self.golden_position = None
        self.golden_spawn_time = 0

    def load_assets(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets = os.path.join(base, "assets")

        def load(name):
            img = pygame.image.load(os.path.join(assets, name))
            return pygame.transform.scale(
                img,
                (settings.SNAKE_SIZE, settings.SNAKE_SIZE)
            )

        self.snake_head_img = load("snake_head.png")
        self.snake_body_img = load("snake_body.png")
        self.apple_img = load("apple.png")
        self.pear_img = load("pear.png")
        self.wall_img = load("wall.png")
        self.golden_img = load("golden_apple.png")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if self.state == GameState.MENU and event.key == pygame.K_SPACE:
                    self.start_game()

                elif self.state == GameState.PLAYING:
                    self.handle_playing_input(event)

                elif self.state == GameState.GAME_OVER and event.key == pygame.K_r:
                    self.state = GameState.MENU

    def handle_playing_input(self, event):
        if event.key in [pygame.K_UP, pygame.K_w] and self.snake.dy == 0:
            self.snake.dx, self.snake.dy = 0, -settings.SNAKE_SIZE
        elif event.key in [pygame.K_DOWN, pygame.K_s] and self.snake.dy == 0:
            self.snake.dx, self.snake.dy = 0, settings.SNAKE_SIZE
        elif event.key in [pygame.K_LEFT, pygame.K_a] and self.snake.dx == 0:
            self.snake.dx, self.snake.dy = -settings.SNAKE_SIZE, 0
        elif event.key in [pygame.K_RIGHT, pygame.K_d] and self.snake.dx == 0:
            self.snake.dx, self.snake.dy = settings.SNAKE_SIZE, 0

    def update(self):
        if self.state == GameState.PLAYING:
            self.update_playing()

    def update_playing(self):
        self.snake.move()

        # GOLDEN SPAWN
        if self.golden_position is None and random.randint(1, 300) == 1:
            self.golden_position = self.spawn_manager.spawn_food(
                self.snake.body,
                self.obstacles,
                1
            )[0]
            self.golden_spawn_time = pygame.time.get_ticks()

        if self.golden_position:
            if pygame.time.get_ticks() - self.golden_spawn_time > 5000:
                self.golden_position = None

        # SUDAR
        if (
            self.snake.check_wall_collision()
            or self.snake.check_self_collision()
            or (self.snake.x, self.snake.y) in self.obstacles
        ):
            self.sound_manager.play_game_over()
            self.score_manager.check_high_score()
            self.state = GameState.GAME_OVER
            return

        # GOLDEN EAT
        if self.golden_position and (self.snake.x, self.snake.y) == self.golden_position:
            self.snake.grow(3)
            self.score_manager.add(5)
            self.sound_manager.play_eat()
            self.golden_position = None

        # APPLES
        for pos in self.apple_positions:
            if (self.snake.x, self.snake.y) == pos:
                self.snake.grow(1)
                self.score_manager.add(1)
                self.sound_manager.play_eat()
                self.apple_positions.remove(pos)
                self.apple_positions += self.spawn_manager.spawn_food(
                    self.snake.body,
                    self.obstacles,
                    1
                )
                break

        # PEARS
        for pos in self.pear_positions:
            if (self.snake.x, self.snake.y) == pos:
                self.snake.grow(2)
                self.score_manager.add(2)
                self.sound_manager.play_eat()
                self.pear_positions.remove(pos)
                self.pear_positions += self.spawn_manager.spawn_food(
                    self.snake.body,
                    self.obstacles,
                    1
                )
                break

    def draw(self):
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_playing()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

    def draw_menu(self):
        self.screen.fill(settings.BLUE)
        text = self.font.render("Press SPACE to Start", True, settings.WHITE)
        self.screen.blit(text, (settings.WIDTH//2 - 150, settings.HEIGHT//2))

    def draw_playing(self):
        self.screen.fill(settings.BLUE)

        for pos in self.apple_positions:
            self.screen.blit(self.apple_img, pos)

        for pos in self.pear_positions:
            self.screen.blit(self.pear_img, pos)

        if self.golden_position:
            self.screen.blit(self.golden_img, self.golden_position)

        for pos in self.obstacles:
            self.screen.blit(self.wall_img, pos)

        self.snake.draw(self.screen, self.snake_head_img, self.snake_body_img)

        score_text = self.font.render(
            f"Score: {self.score_manager.score}", True, settings.WHITE
        )
        high_text = self.font.render(
            f"High Score: {self.score_manager.high_score}",
            True,
            settings.WHITE
        )    
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(high_text, (20, 60))

    def draw_game_over(self):
        self.screen.fill(settings.BLUE)
        over = self.font.render("GAME OVER - Press R", True, settings.RED)
        self.screen.blit(over, (settings.WIDTH//2 - 180, settings.HEIGHT//2))

    def start_game(self):
        self.reset_game()
        self.state = GameState.PLAYING

    def reset_game(self):
        self.snake = Snake(settings.WIDTH, settings.HEIGHT, settings.SNAKE_SIZE)
        self.obstacles = self.spawn_manager.spawn_obstacles(15)
        self.apple_positions = self.spawn_manager.spawn_food(
            self.snake.body,
            self.obstacles,
            settings.APPLE_COUNT
        )
        self.pear_positions = self.spawn_manager.spawn_food(
            self.snake.body,
            self.obstacles,
            settings.PEAR_COUNT
        )
        self.score_manager.reset()
        self.fps = settings.START_FPS
        self.golden_position = None