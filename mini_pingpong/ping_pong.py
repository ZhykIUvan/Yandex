import sys

import pygame
import random
import runpy

# Константы
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
PADDLE_SPEED = 5
BALL_SPEED_X = 3
BALL_SPEED_Y = 3
SCORE_LIMIT = 10
FPS = 60
GRAY = (40, 40, 40)
ORANGE = (255, 102, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def run_pingpong():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Пинг-понг")
    clock = pygame.time.Clock()

    def draw_score(score_left, score_right):
        font = pygame.font.Font(None, 36)
        text = font.render(f"{score_left} : {score_right}", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, 50))
        screen.blit(text, text_rect)

    class Button:
        def __init__(self, screen, text, x, y, width, height):
            self.screen = screen
            self.screen_rect = self.screen.get_rect()

            self.width = width
            self.height = height
            self.bg_color = 243, 245, 140
            self.text_color = 10, 10, 10

            self.font = pygame.font.SysFont('Courier', 35)

            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.center = x, y

            self.creating_text(text)

        def creating_text(self, text):
            self.text_surf = self.font.render(text, True, self.text_color, self.bg_color)
            self.text_rect = self.text_surf.get_rect()
            self.text_rect.center = self.rect.center

        def draw(self):
            self.screen.fill(self.bg_color, self.rect)
            self.screen.blit(self.text_surf, self.text_rect)

    # Класс платформы
    class Paddle(pygame.sprite.Sprite):
        def __init__(self, x, color):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = HEIGHT / 2 - PADDLE_HEIGHT / 2
            self.speed = 0
            self.score = 0

        def updatee(self):
            self.rect.y += self.speed
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

    # Класс мячика
    class Ball(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((BALL_RADIUS*2, BALL_RADIUS*2))
            pygame.draw.circle(self.image, ORANGE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
            self.rect = self.image.get_rect()
            self.reset()

        def updatee(self):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if self.rect.top < 0 or self.rect.bottom > HEIGHT:
                self.speed_y *= -1

            if pygame.sprite.collide_rect(self, paddle_left) or pygame.sprite.collide_rect(self, paddle_right):
                self.speed_x *= -1.1
                self.speed_y *= 1.1  # Увеличение скорости мяча на 10%

            if self.rect.left < 0:
                paddle_right.score += 1
                self.reset()
            elif self.rect.right > WIDTH:
                paddle_left.score += 1
                self.reset()

        def reset(self):
            self.rect.center = (WIDTH/2, HEIGHT/2)
            self.speed_x = random.choice([-1, 1]) * BALL_SPEED_X
            self.speed_y = random.choice([-1, 1]) * BALL_SPEED_Y


    # Создание платформ и мячика
    paddle_left = Paddle(0, RED)
    paddle_right = Paddle(WIDTH - PADDLE_WIDTH, BLUE)
    ball = Ball()

    # Группировка спрайтов для обновления и отрисовки
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle_left, paddle_right, ball)

    # Игровой цикл
    running = False
    move_up_left = False
    move_down_left = True
    move_up_right = False
    move_down_right = True

    play_button = Button(screen, 'Играть', 400, 300, 200, 70)
    exit_button = Button(screen, 'Выход', 400, 400, 200, 70)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if move_up_left:
                        move_up_left = False
                        move_down_left = True
                    else:
                        move_up_left = True
                elif event.key == pygame.K_l:
                    if move_up_right:
                        move_up_right = False
                        move_down_right = True
                    else:
                        move_up_right = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not running:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_button.rect.collidepoint(mouse_x, mouse_y):
                    running = True
                elif exit_button.rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    runpy.run_module(mod_name='menu')
                    sys.exit()
        if running:
            if move_up_left:
                paddle_left.speed = -PADDLE_SPEED
            elif move_down_left:
                paddle_left.speed = PADDLE_SPEED
            else:
                paddle_left.speed = 0

            if move_up_right:
                paddle_right.speed = -PADDLE_SPEED
            elif move_down_right:
                paddle_right.speed = PADDLE_SPEED
            else:
                paddle_right.speed = 0

            paddle_left.updatee()
            paddle_right.updatee()
            ball.updatee()

            screen.fill(GRAY)

            pygame.draw.rect(screen, GREEN, (0, 0, WIDTH, 10))
            pygame.draw.rect(screen, GREEN, (0, HEIGHT-10, WIDTH, 10))
            all_sprites.draw(screen)
            draw_score(paddle_left.score, paddle_right.score)

            def show_game_over():
                winner = "LEFT" if paddle_left.score == SCORE_LIMIT else "RIGHT"
                message = f"Player {winner} wins with a score of {SCORE_LIMIT}!"
                font = pygame.font.Font(None, 48)
                text = font.render(message, True, WHITE)
                text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                screen.blit(text, text_rect)

            if paddle_left.score == SCORE_LIMIT or paddle_right.score == SCORE_LIMIT:
                show_game_over()

                pygame.display.flip()
                pygame.time.wait(3000)  # Ожидание 3 секунды перед завершением игры
                running = False
                paddle_left.score = 0
                paddle_right.score = 0

            pygame.display.flip()
            clock.tick(FPS)
        else:
            play_button.draw()
            exit_button.draw()

            pygame.display.flip()