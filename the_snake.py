"""
Классическая игра 'Змейка'.
Управление: стрелки ← ↑ ↓ →
Рестарт после проигрыша: R
Выход: ESC или крестик окна
"""

import random
import sys

import pygame


# Инициализация PyGame
pygame.init()

# Константы игры
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
FPS = 15

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 180, 0)
GRAY = (40, 40, 40)
BOARD_BACKGROUND_COLOR = BLACK

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Размеры сетки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """
        Инициализирует игровой объект.

        Args:
            position: Начальная позиция объекта
            body_color: Цвет объекта
        """
        self.position = position if position else (0, 0)
        self.body_color = body_color if body_color else WHITE

    def draw(self):
        """Отрисовывает объект на экране."""
        pass


class Apple(GameObject):
    """Класс для яблока в игре."""

    def __init__(self):
        """Инициализирует яблоко с красным цветом и случайной позицией."""
        super().__init__(body_color=RED)
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """
        Устанавливает новую случайную позицию для яблока.

        Args:
            snake_positions: Список позиций змейки
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        rect = (x, y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, WHITE, rect, 1)


class Snake(GameObject):
    """Класс для змейки в игре."""

    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__(body_color=GREEN)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        x = GRID_WIDTH // 2
        y = GRID_HEIGHT // 2
        self.positions = [(x, y)]
        self.direction = RIGHT
        self.next_direction = None
        self.score = 0
        self.grow = 0

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        self.next_direction = new_direction

    def move(self):
        """
        Двигает змейку в текущем направлении.

        Returns:
            bool: True если движение успешно, False при столкновении с собой
        """
        if self.next_direction:
            dx, dy = self.next_direction
            if (self.direction[0] * -1, self.direction[1] * -1) != (dx, dy):
                self.direction = self.next_direction
            self.next_direction = None

        x, y = self.get_head_position()
        dx, dy = self.direction
        new = ((x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT)

        if new in self.positions:
            return False

        self.positions.insert(0, new)

        if self.grow > 0:
            self.grow -= 1
        else:
            self.positions.pop()

        return True

    def draw(self):
        """Отрисовывает змейку на экране."""
        for i, (x, y) in enumerate(self.positions):
            px = x * GRID_SIZE
            py = y * GRID_SIZE
            rect = (px, py, GRID_SIZE, GRID_SIZE)
            if i == 0:
                pygame.draw.rect(screen, self.body_color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)
            else:
                pygame.draw.rect(screen, DARK_GREEN, rect)


def draw_grid():
    """Рисует игровую сетку."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_score(score):
    """
    Отображает текущий счёт.

    Args:
        score: Количество очков
    """
    font = pygame.font.Font(None, 32)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))


def game_over_screen(score):
    """
    Отображает экран окончания игры.

    Args:
        score: Финальный счёт
    """
    font = pygame.font.Font(None, 48)
    text = font.render('GAME OVER', True, RED)
    x_pos = SCREEN_WIDTH // 2 - 120
    y_pos = SCREEN_HEIGHT // 2 - 40
    screen.blit(text, (x_pos, y_pos))

    font2 = pygame.font.Font(None, 30)
    score_text = font2.render(f'Score: {score}', True, WHITE)
    x_pos = SCREEN_WIDTH // 2 - 70
    y_pos = SCREEN_HEIGHT // 2 + 10
    screen.blit(score_text, (x_pos, y_pos))

    restart = font2.render('Press R to restart', True, GREEN)
    x_pos = SCREEN_WIDTH // 2 - 110
    y_pos = SCREEN_HEIGHT // 2 + 50
    screen.blit(restart, (x_pos, y_pos))


def handle_keys(snake, game_over):
    """Обработка событий игры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    return True  # Рестарт
            else:
                if event.key == pygame.K_UP:
                    snake.update_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.update_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.update_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.update_direction(RIGHT)
    return False


def update_game_state(snake, apple, game_over):
    """Обновление состояния игры."""
    if not game_over:
        if not snake.move():
            return True  # Игра окончена

        if snake.get_head_position() == apple.position:
            snake.grow += 1
            snake.score += 10
            apple.randomize_position(snake.positions)

    return game_over


def draw_game_state(snake, apple, game_over):
    """Отрисовка состояния игры."""
    screen.fill(BOARD_BACKGROUND_COLOR)

    if not game_over:
        draw_grid()
        snake.draw()
        apple.draw()
        draw_score(snake.score)
    else:
        snake.draw()
        apple.draw()
        draw_score(snake.score)
        game_over_screen(snake.score)

    pygame.display.flip()


def main():
    """Главная функция игры."""
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    game_over = False

    while True:
        # Обработка событий
        if handle_keys(snake, game_over):
            snake.reset()
            apple.randomize_position(snake.positions)
            game_over = False

        # Обновление состояния
        game_over = update_game_state(snake, apple, game_over)

        # Отрисовка
        draw_game_state(snake, apple, game_over)

        # Контроль FPS
        clock.tick(FPS)


def start_game():
    """Функция для запуска игры из тестов."""
    main()


if __name__ == '__main__':
    start_game()
