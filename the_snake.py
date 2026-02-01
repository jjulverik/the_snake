"""
Классическая игра 'Змейка'.

Управление: стрелки ← ↑ ↓ →
Рестарт после проигрыша: R
Выход: ESC или крестик окна
"""

import random
import sys

import pygame as pg

pg.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
FPS = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 180, 0)
GRAY = (40, 40, 40)
BOARD_BACKGROUND_COLOR = BLACK

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

X_IDX = 0
Y_IDX = 1

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Snake')
clock = pg.time.Clock()


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
        raise NotImplementedError(
            'Метод draw должен быть переопределен в дочернем классе'
        )


class Apple(GameObject):
    """Класс для яблока в игре."""

    def __init__(self, snake_positions=None):
        """
        Инициализирует яблоко с красным цветом и случайной позицией.

        Args:
            snake_positions: Список позиций змейки для избегания коллизий
        """
        super().__init__(body_color=RED)
        if snake_positions is None:
            snake_positions = []
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """
        Устанавливает новую случайную позицию для яблока.

        Args:
            snake_positions: Список позиций змейки,
            чтобы яблоко не появилось на ней
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        x = self.position[X_IDX] * GRID_SIZE
        y = self.position[Y_IDX] * GRID_SIZE
        rect = pg.Rect(x, y, GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, WHITE, rect, 1)


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
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.score = 0
        self.grow = 0
        self.last_tail_position = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        self.next_direction = new_direction

    def move(self):
        """Двигает змейку в текущем направлении."""
        if self.next_direction:
            dx, dy = self.next_direction
            opposite_x = self.direction[X_IDX] * -1
            opposite_y = self.direction[Y_IDX] * -1
            if (opposite_x, opposite_y) != (dx, dy):
                self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_position = (
            (head_x + dx) % GRID_WIDTH,
            (head_y + dy) % GRID_HEIGHT
        )

        self.positions.insert(0, new_position)

        if self.grow > 0:
            self.grow -= 1
            self.last_tail_position = None
        else:
            self.last_tail_position = self.positions.pop()

    def check_self_collision(self):
        """
        Проверяет столкновение змейки с самой собой.

        Returns:
            bool: True если произошло столкновение
        """
        head_position = self.get_head_position()
        return head_position in self.positions[1:]

    def draw(self):
        """Отрисовывает змейку на экране."""
        for index, (x, y) in enumerate(self.positions):
            px = x * GRID_SIZE
            py = y * GRID_SIZE
            rect = pg.Rect(px, py, GRID_SIZE, GRID_SIZE)
            if index == 0:
                pg.draw.rect(screen, self.body_color, rect)
                pg.draw.rect(screen, WHITE, rect, 1)
                continue
            pg.draw.rect(screen, DARK_GREEN, rect)


def draw_grid():
    """Рисует игровую сетку."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pg.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pg.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_score(score):
    """
    Отображает текущий счёт.

    Args:
        score: Количество очков
    """
    font = pg.font.Font(None, 32)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))


def game_over_screen(score):
    """
    Отображает экран окончания игры.

    Args:
        score: Финальный счёт
    """
    font = pg.font.Font(None, 48)
    text = font.render('GAME OVER', True, RED)
    screen.blit(
        text,
        (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 40)
    )

    font_small = pg.font.Font(None, 30)
    score_text = font_small.render(f'Score: {score}', True, WHITE)
    screen.blit(
        score_text,
        (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 10)
    )

    restart_text = font_small.render('Press R to restart', True, GREEN)
    screen.blit(
        restart_text,
        (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50)
    )


def handle_keys(snake, game_over):
    """
    Обрабатывает нажатия клавиш.

    Args:
        snake: Объект змейки
        game_over: Флаг окончания игры

    Returns:
        bool: True если требуется рестарт
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if game_over and event.key == pg.K_r:
                return True

            if not game_over:
                direction_map = {
                    pg.K_UP: UP,
                    pg.K_DOWN: DOWN,
                    pg.K_LEFT: LEFT,
                    pg.K_RIGHT: RIGHT
                }
                new_direction = direction_map.get(event.key)
                if new_direction:
                    snake.update_direction(new_direction)

    return False


def check_collisions(snake, apple):
    """
    Проверяет все возможные столкновения в игре.

    Args:
        snake: Объект змейки
        apple: Объект яблока

    Returns:
        tuple: (game_over, ate_apple)
    """
    if snake.check_self_collision():
        return True, False

    if snake.get_head_position() == apple.position:
        snake.grow += 1
        snake.score += 1
        apple.randomize_position(snake.positions)
        return False, True

    return False, False


def update_game_state(snake, apple, game_over):
    """
    Обновляет состояние игры.

    Args:
        snake: Объект змейки
        apple: Объект яблока
        game_over: Флаг окончания игры

    Returns:
        bool: Обновлённый флаг game_over
    """
    if game_over:
        return game_over

    snake.move()
    game_over, _ = check_collisions(snake, apple)

    return game_over


def draw_game_state(snake, apple, game_over):
    """
    Отрисовывает текущее состояние игры.

    Args:
        snake: Объект змейки
        apple: Объект яблока
        game_over: Флаг окончания игры
    """
    screen.fill(BOARD_BACKGROUND_COLOR)

    draw_grid()
    snake.draw()
    apple.draw()
    draw_score(snake.score)

    if game_over:
        game_over_screen(snake.score)

    pg.display.flip()


def main():
    """Главная функция игры."""
    snake = Snake()
    apple = Apple(snake.positions)
    game_over = False

    while True:
        if handle_keys(snake, game_over):
            snake.reset()
            apple.randomize_position(snake.positions)
            game_over = False

        game_over = update_game_state(snake, apple, game_over)
        draw_game_state(snake, apple, game_over)
        clock.tick(FPS)


def start_game():
    """Функция для запуска игры из тестов."""
    main()


if __name__ == '__main__':
    start_game()
