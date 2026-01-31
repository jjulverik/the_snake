import pygame
import random
import sys

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = 20
FPS = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 180, 0)
GRAY = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

GRID_W = WIDTH // SIZE
GRID_H = HEIGHT // SIZE


class Apple:
    def __init__(self):
        self.color = RED
        self.pos = (0, 0)
        self.new_pos([])

    def new_pos(self, snake):
        while True:
            x = random.randint(0, GRID_W - 1)
            y = random.randint(0, GRID_H - 1)
            if (x, y) not in snake:
                self.pos = (x, y)
                break

    def draw(self):
        x = self.pos[0] * SIZE
        y = self.pos[1] * SIZE
        pygame.draw.rect(screen, self.color, (x, y, SIZE, SIZE))
        pygame.draw.rect(screen, WHITE, (x, y, SIZE, SIZE), 1)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        x = GRID_W // 2
        y = GRID_H // 2
        self.body = [(x, y)]
        self.dir = (1, 0)
        self.next_dir = None
        self.score = 0
        self.grow = 0

    def head(self):
        return self.body[0]

    def move(self):
        if self.next_dir:
            if (self.dir[0] * -1, self.dir[1] * -1) != self.next_dir:
                self.dir = self.next_dir
            self.next_dir = None

        x, y = self.head()
        dx, dy = self.dir
        new = ((x + dx) % GRID_W, (y + dy) % GRID_H)

        if new in self.body:
            return False

        self.body.insert(0, new)

        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()

        return True

    def eat(self):
        self.grow += 1
        self.score += 10

    def draw(self):
        for i, (x, y) in enumerate(self.body):
            px = x * SIZE
            py = y * SIZE
            if i == 0:
                pygame.draw.rect(screen, GREEN, (px, py, SIZE, SIZE))
                pygame.draw.rect(screen, WHITE, (px, py, SIZE, SIZE), 1)
            else:
                pygame.draw.rect(screen, DARK_GREEN, (px, py, SIZE, SIZE))


def draw_grid():
    for x in range(0, WIDTH, SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_score(score):
    font = pygame.font.Font(None, 32)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def game_over_screen(score):
    font = pygame.font.Font(None, 48)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))

    font2 = pygame.font.Font(None, 30)
    score_text = font2.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 10))

    restart = font2.render("Press R to restart", True, GREEN)
    screen.blit(restart, (WIDTH // 2 - 110, HEIGHT // 2 + 50))


def main():
    snake = Snake()
    apple = Apple()
    apple.new_pos(snake.body)

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        snake.reset()
                        apple.new_pos(snake.body)
                        game_over = False
                else:
                    if event.key == pygame.K_UP:
                        snake.next_dir = (0, -1)
                    elif event.key == pygame.K_DOWN:
                        snake.next_dir = (0, 1)
                    elif event.key == pygame.K_LEFT:
                        snake.next_dir = (-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        snake.next_dir = (1, 0)

        screen.fill(BLACK)

        if not game_over:
            draw_grid()

            if not snake.move():
                game_over = True

            if snake.head() == apple.pos:
                snake.eat()
                apple.new_pos(snake.body)

            snake.draw()
            apple.draw()
            draw_score(snake.score)
        else:
            snake.draw()
            apple.draw()
            draw_score(snake.score)
            game_over_screen(snake.score)

        pygame.display.flip()
        clock.tick(FPS)


def start_game():
    """Функция для запуска игры из тестов."""
    main()


if __name__ == "__main__":
    start_game()