from random import choice, randint
import pygame

# Инициализация PyGame:
pygame.init()


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь с направлениями:
DIRECTION_KEYS = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 3

# Центр игрового поля:
SCREEN_CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для описания игровых объектов."""

    def __init__(self, body_color=None,
                 position=(SCREEN_CENTER)) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Прорисовка объекта."""


class Apple(GameObject):
    """Класс Apple - отвечает за генерацию яблока на игровом поле."""

    def randomize_position(self, occupied_cells):
        """Задание рандомной позиции яблоку."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break
            else:
                continue

    def __init__(self, body_color=APPLE_COLOR) -> None:
        self.body_color = body_color
        self.randomize_position(SCREEN_CENTER)

    # Метод draw класса Apple
    def draw(self):
        """Прорисовка яблока."""
        rect = pygame.Rect(
            (self.position),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывает змейку"""

    def __init__(self):
        self.body_color = SNAKE_COLOR
        self.reset()
        self.direction = RIGHT
        self.last = None

    def update_direction(self, next_direction=None):
        """Изменение направления после нажатия клавиши"""
        if next_direction:
            self.direction = next_direction
            next_direction = None

    def draw(self):
        """Прорисовка змейки"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def get_head_position(self):
        """Получение позиции головы змейки"""
        return self.positions[0]

    def move(self):
        """Перемещение змейки на одну клетку."""
        dx_position, dy_position = self.get_head_position()
        dx_direction, dy_direction = self.direction
        if self.positions[0] in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, ((
                dx_position + dx_direction * GRID_SIZE)
                % SCREEN_WIDTH,
                (dy_position + dy_direction * GRID_SIZE)
                % SCREEN_HEIGHT))
        if len(self.positions) > self.length:
            self.last = self.positions.pop(-1)

    def reset(self):
        """Сброс змейки после столкновения с собой."""
        self.length = 1
        self.position = None
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обработка нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if (event.key, game_object.direction) in DIRECTION_KEYS.keys():
                next_direction = DIRECTION_KEYS[
                    event.key,
                    game_object.direction]
                if next_direction:
                    game_object.update_direction(next_direction)


def main():
    """
    Создаются экземпляры классов,
    описывается логика игры
    """
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple = Apple()
    snake = Snake()
    apple.draw()
    snake.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pygame.display.update()


# Запуск главного цикла игры.
if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self, surface):
#     rect = pygame.Rect(
#         (self.position[0], self.position[1]),
#         (GRID_SIZE, GRID_SIZE)
#     )
#     pygame.draw.rect(surface, self.body_color, rect)
#     pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self, surface):
#     for position in self.positions[:-1]:
#         rect = (
#             pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
#         )
#         pygame.draw.rect(surface, self.body_color, rect)
#         pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, self.body_color, head_rect)
#     pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(
#             (self.last[0], self.last[1]),
#             (GRID_SIZE, GRID_SIZE)
#         )
#         pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and
#                 game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT
#                 and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
