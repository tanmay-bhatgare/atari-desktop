import pygame
import sys
import random
import os
from pygame import mixer

pygame.init()

mixer.music.load(os.path.join('assets', 'chipi-chapa.mp3'))
mixer.music.play(-1)

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

BRICKS = []
BRICKS_SIZE = 50
BRICKS_X = [xCord for xCord in range(0, 551, BRICKS_SIZE)]
BRICKS_Y = [yCord for yCord in range(0, 101, BRICKS_SIZE)]


# @ Colors
BG = (12, 12, 12)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# @ Score
SCORE = 0
font = pygame.font.Font(os.path.join('assets', 'UbuntuMono-Regular.ttf'), 32)
font1 = pygame.font.Font(os.path.join('assets', 'UbuntuMono-Regular.ttf'), 70)

# @ Functions


def show_score(X, Y):
    score_text = font.render(f"Score: {SCORE}", True, WHITE)
    SCREEN.blit(score_text, (X, Y))
    if SCORE == 36:
        game_complete = font1.render("You Win!", True, WHITE)
        SCREEN.blit(game_complete, (160, 270))
        DISC.x = 1000
        BALL.y = -1000000

# @ Class Objects


class Rectangle:
    collision_tolerance = 10
    xSpeed = 7.2
    ySpeed = 4.5

    def __init__(self, x, y, width, height, color, border_rad=-1) -> None:
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.border_rad = border_rad

    def draw(self, SCREEN) -> None:
        # print("working...")
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y,
                         self.width, self.height), border_radius=self.border_rad)

    def move(self, keys) -> None:
        # print("working...")
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and self.x >= 0:
            self.x -= self.xSpeed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and self.x <= SCREEN_WIDTH - self.width:
            self.x += self.xSpeed

        if keys[pygame.K_w] or keys[pygame.K_UP] and self.y >= 500:
            self.y -= self.ySpeed
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and self.y <= SCREEN_HEIGHT - self.height:
            self.y += self.ySpeed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collide(self, other: "Circle"):
        if self.get_rect().colliderect(other.get_rect()):
            # @ Y-Axis Collision
            if abs(self.get_rect().top - other.get_rect().bottom) < Rectangle.collision_tolerance and other.ySpeed > 0:
                Circle.ySpeed *= -1
            if abs(self.get_rect().bottom - other.get_rect().top) < Rectangle.collision_tolerance and other.ySpeed < 0:
                Circle.ySpeed *= -1

            # @ X-Axis Collision
            if abs(self.get_rect().left - other.get_rect().right) < Rectangle.collision_tolerance and other.xSpeed > 0:
                Circle.xSpeed *= -1
            if abs(self.get_rect().right - other.get_rect().left) < Rectangle.collision_tolerance and other.xSpeed < 0:
                Circle.xSpeed *= -1

    def remove_rect(self, other: "Circle"):
        global SCORE
        if self.get_rect().colliderect(other.get_rect()):
            hit_sound = mixer.Sound(os.path.join("assets", 'hit.mp3'))
            hit_sound.play()
            SCORE += 1
            self.x = 1000


class Circle:
    xSpeed = 5.2
    ySpeed = 4.5

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, SCREEN):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += Circle.xSpeed
        self.y += Circle.ySpeed
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            Circle.xSpeed *= -1
        if self.y <= self.radius:
            Circle.ySpeed *= -1
        if self.y >= SCREEN_HEIGHT - self.radius:
            sys.exit()

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


# @ Objects
DISC = Rectangle(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60, 120, 15, WHITE)
BALL = Circle(400, 400, 10, BLUE)
# @ Brick spawner
for _ in range(1):
    for yCord in BRICKS_Y:
        for xCord in BRICKS_X:
            # print(xCord, yCord)
            random_red = random.randint(50, 255)
            random_green = random.randint(50, 255)
            random_blue = random.randint(50, 255)
            BRICKS.append(Rectangle(xCord, yCord, BRICKS_SIZE,
                          BRICKS_SIZE, (random_red, random_green, random_blue), 10))


# @ Game Loop
RUN = True
while RUN:
    SCREEN.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    keys_pressed = pygame.key.get_pressed()
    # * Drawing All Objects
    DISC.draw(SCREEN)
    DISC.move(keys_pressed)
    DISC.collide(BALL)

    BALL.draw(SCREEN)
    BALL.move()

    # @ Drawing Bricks
    for BRICK in BRICKS:
        BRICK.draw(SCREEN)
        BRICK.collide(BALL)
        BRICK.remove_rect(BALL)

    show_score(440, 568)

    # @ Game Updating
    CLOCK.tick(FPS)
    pygame.display.flip()

pygame.quit()
sys.exit()
