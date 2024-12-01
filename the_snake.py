from random import randint

import pygame

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых обьектов."""

    def __init__(self) -> None:  # Инициализация класса
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка обьектов на экране.
        Метод определен в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):  # Инициализация класса
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, snake_positions=None):
        """Генерация случайной позиции яблока."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if snake_positions is None or self.position not in snake_positions:
                break


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):  # Инициализация класса
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Пермещение змейки в текущем направлении."""
        self.last = self.positions[-1] if self.positions else None
        if self.direction:
            new_head = (self.positions[0][0] + self.direction[0] * GRID_SIZE,
                        self.positions[0][1] + self.direction[1] * GRID_SIZE)
            new_head = self.get_head_position(new_head)
            self.positions.insert(0, new_head)
            self.positions.pop()
        self.update_direction()

    def grow(self):
        """Увеличение длины змейки."""
        self.positions.append(self.last)

    def get_head_position(self, head_position):
        """Обработка выхода головы змейки
        за пределы игрового поля."""
        x, y = head_position
        x = (x + GRID_WIDTH * GRID_SIZE) % (GRID_WIDTH * GRID_SIZE)
        y = (y + GRID_HEIGHT * GRID_SIZE) % (GRID_HEIGHT * GRID_SIZE)
        return (x, y)

    def check_self_collision(self):
        """Проверка на совпадение положения головы змейки и тела."""
        return self.positions[0] in self.positions[1:]

    def reset(self):
        """Сброс текущего состояния змейки для новой игры."""
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработка нажатия клавиш, для управления змейкой."""
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
    """Основная функция игры."""
    pygame.init()

    # Экземпляры класса
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)  # Скорость змейки
        handle_keys(snake)  # Обработка нажатия клавиш
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана
        apple.draw()  # Отрисовка яблока
        snake.draw()  # Отрисовка змейки
        snake.move()  # Движение змейки

        if snake.positions[0] == apple.position:  # Проверка на сьедание яблока
            snake.grow()  # Увеличение длины змейки
            apple.randomize_position()  # Случайная позиция яблока

        if snake.check_self_collision():  # Проверка на столкновение змейки
            snake.reset()  # Сброс состояния змейки

        pygame.display.update()  # Обновление экрана


if __name__ == '__main__':
    main()
