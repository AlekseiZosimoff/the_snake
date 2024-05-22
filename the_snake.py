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

    def draw_cell(self, cell_color,
                  border_color=BORDER_COLOR,
                  position=SCREEN_CENTER):
        """Отрисовка одной ячейки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, cell_color, rect)
        pygame.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс Apple - отвечает за генерацию яблока на игровом поле."""

    def __init__(self, occupied_cells=SCREEN_CENTER, body_color=APPLE_COLOR):
        self.occupied_cells = occupied_cells
        self.body_color = body_color
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells):
        """Задание рандомной позиции яблоку."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break

    # Метод draw класса Apple
    def draw(self):
        """Прорисовка яблока."""
        self.draw_cell(self.body_color, BORDER_COLOR, self.position)


class Snake(GameObject):
    """Класс описывает змейку"""

    def __init__(self):
        self.body_color = SNAKE_COLOR
        self.positions = SCREEN_CENTER
        self.reset()
        self.direction = RIGHT
        self.last = None

    def update_direction(self, next_direction=None):
        """Изменение направления после нажатия клавиши"""
        self.direction = next_direction

    def draw(self):
        """Прорисовка змейки"""
        # Отрисовка головы змейки
        head_rect = self.get_head_position()
        self.draw_cell(self.body_color, BORDER_COLOR, head_rect)

        # Затирание последнего сегмента
        if self.last:
            last_rect = self.last
            self.draw_cell(BOARD_BACKGROUND_COLOR,
                           BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получение позиции головы змейки"""
        return self.positions[0]

    def move(self):
        """Перемещение змейки на одну клетку."""
        dx_position, dy_position = self.get_head_position()
        dx_direction, dy_direction = self.direction
        self.position = ((
            dx_position + dx_direction * GRID_SIZE)
            % SCREEN_WIDTH,
            (dy_position + dy_direction * GRID_SIZE)
            % SCREEN_HEIGHT)
        self.positions.insert(0, self.position)
        self.last = (self.positions.pop() if
                     len(self.positions) > self.length else None)

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
    snake = Snake()
    apple = Apple(snake.positions)
    apple.randomize_position(snake.positions)
    while True:
        apple.draw()
        snake.draw()
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.positions[0] in snake.positions[2:]:
            snake.reset()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        pygame.display.update()


# Запуск главного цикла игры.
if __name__ == '__main__':
    main()
