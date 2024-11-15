from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Общее описание экземпляров классов."""

    def __init__(self):
        self.position = GRID_CENTER
        self.body_color = None

    def draw(self):
        """Определяем метод для отрисовки объектов на поле."""


class Apple(GameObject):
    """Объявляем дочерний класс - Яблоко."""

    def __init__(self, occupied_positions=None):
        super().__init__()
        self.randomize_position(occupied_positions)
        self.body_color = APPLE_COLOR

    def randomize_position(self, occupied_positions):
        """Метод для генерации яблока в случайной позиции,
        с учетом положения объектов на поле.
        """
        occupied_positions = occupied_positions or []
        while True:
            self.position = (
                (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Метод для отрисовки яблока на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Объявляем дочерний класс, определяем атрибуты и методы Змейки."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод, определяющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, описывающий логику движения змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_position = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def growth(self):
        """Метод для увеличения максимальной длины змейки."""
        self.length += 1

    def reset(self):
        """Метод для обнуления прогресса и установления змейки в
        исходное состояние.
        """
        self.length = 1
        self.positions = [self.position]
        direction = (UP, DOWN, RIGHT, LEFT)
        self.direction = choice(direction)

    def get_head_position(self):
        """Метод для определения координат головы змейки"""
        return self.positions[0]

    def draw(self):
        """Метод для отрисовки змейки на поле"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(
            self.get_head_position(),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция для управления движением змейки с помощью клавиатуры"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция, описывающая логику игры"""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.move()
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            snake.growth()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        pygame.display.update()


if __name__ == '__main__':
    main()
