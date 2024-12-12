from random import randint as rnd

import pygame as pg

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

# Размер шрифта
FONT_SIZE = 25

# Цвет шрифта
FONT_COLOR = (255, 255, 255)

# Позиция шрифта
FONT_POSITION = (10, 5)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых обьектов."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка обьектов на экране.
        Метод определен в дочерних классах.
        """
        raise NotImplementedError

    def draw_cell(self, position, color):
        """Отрисовка одной ячейки на экране."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Отрисовка яблока на экране."""
        super().draw_cell(self.position, self.body_color)

    def randomize_position(self, snake_positions=None):
        """Генерация случайной позиции яблока."""
        while True:
            self.position = (rnd(0, GRID_WIDTH - 1) * GRID_SIZE,
                             rnd(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if snake_positions is None or self.position not in snake_positions:
                break


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions:
            super().draw_cell(position, self.body_color)

        # Затирание последнего сегмента
        if self.last:
            super().draw_cell(self.last, self.body_color)

    def update_direction(self):
        """Обновление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Пермещение змейки в текущем направлении."""
        self.last = self.positions[-1] if self.positions else None
        current_head = self.get_head_position()
        new_head = (current_head[0] + self.direction[0] * GRID_SIZE,
                    current_head[1] + self.direction[1] * GRID_SIZE)
        new_head = (new_head[0] % (GRID_WIDTH * GRID_SIZE),
                    new_head[1] % (GRID_HEIGHT * GRID_SIZE))
        self.positions.insert(0, new_head)
        self.positions.pop()
        self.update_direction()

    def grow(self):
        """Увеличение длины змейки."""
        self.positions.append(self.last)

    def get_head_position(self):
        """Определяет позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс текущего состояния змейки для новой игры."""
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработка нажатия клавиш, для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pg.init()

    # Экземпляры класса
    apple = Apple()
    snake = Snake()

    count = 0
    font = pg.font.Font(None, FONT_SIZE)

    while True:
        clock.tick(SPEED)  # Скорость змейки
        handle_keys(snake)  # Обработка нажатия клавиш
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана
        apple.draw()  # Отрисовка яблока
        snake.draw()  # Отрисовка змейки
        snake.move()  # Движение змейки
        scores = f'Съедено яблок: {count}'
        text_surface = font.render(scores, True, FONT_COLOR)
        screen.blit(text_surface, FONT_POSITION)

        # Проверка на съедание яблока
        if snake.get_head_position() == apple.position:
            snake.grow()  # Увеличение длины змейки
            apple.randomize_position()  # Случайная позиция яблока
            count += 1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()  # Сброс состояния змейки
            count = 0

        pg.display.update()  # Обновление экрана


if __name__ == '__main__':
    main()
