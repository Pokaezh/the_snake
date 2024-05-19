"""Игра "Змейка". Рабоает с использованием библиотеки Pygame."""

from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

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

# Цвет по умолчанию
DEFAULT_COLOR = (100, 100, 100)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс для описания всех объектов в игре."""

    body_color = DEFAULT_COLOR  # цвет объекта
    position = SCREEN_CENTER  # позиция объекта на игровом поле

    def __init__(self):
        """Метод инициализции объектов класса."""
        self.position = SCREEN_CENTER
        self.body_color = DEFAULT_COLOR

    def draw(self):
        """Метод для рисования объектов
        Пока не используется так как объекты рисуются методами в подклассах.
        """
        pass


class Apple(GameObject):
    """Класс для описания яблока"""

    def __init__(self) -> None:
        """Метод для инициализации яблока."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self) -> tuple[int, int]:
        """Метод для появления нового яблока в случайном месте."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Метод для рисования яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Метод для инициализации змеи."""

    def __init__(self, body_color=SNAKE_COLOR, position=SCREEN_CENTER):
        super().__init__()
        self.body_color = body_color
        self.position = position
        self.positions = list([self.position])
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод для получения координат головы змеи."""
        self.position = self.positions[0]

    def update_direction(self):
        """Метод для обновления направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод для сброса змейки при стооклновении."""
        self.position = SCREEN_CENTER
        self.positions = list([self.position])
        self.length = 1
        self.direction = RIGHT

    def move(self, apple):
        """Метод описывающий движение змейки."""
        self.get_head_position()  # получаем координаты головы
        new_head = (
            (self.position[0] + self.direction[0] * GRID_SIZE),
            (self.position[1] + self.direction[1] * GRID_SIZE),
        )

        if new_head[0] < 0:  # Проверяем достигла ли голова змейки предлов поля
            # и если достигла - отправлям на другой конец игрового поля
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])
        elif new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        self.positions.insert(0, new_head)
        if new_head == apple.position:  # проверяем достигла ли змейка яблоко
            self.length += 1  # если достигла, то добавляем к длине змейки 1
            apple.position = (
                apple.randomize_position()
            )  # получаем новые координаты яблока

        if new_head in self.positions[2:]:  # проверяем не съела ли змейка себя
            screen.fill(BOARD_BACKGROUND_COLOR)
            self.reset()

        if len(self.positions) > self.length:
            # проверяем длину змейки
            self.last = self.positions.pop()
            # если яблоко не съедено, убираем последний элекмент

    def draw(self):
        """Метод для рисования змейки."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
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


def handle_keys(game_object):
    """Функция обратботки нажатий клавиш."""
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
    """Инициализируем PyGame:"""
    pygame.init()

    """ Cоздаём экземпляры классов."""
    apple = Apple()
    snake = Snake()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                return

        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
