from random import randint
import pygame

# Screen and grid settings
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_COLS = SCREEN_WIDTH // GRID_SIZE
GRID_ROWS = SCREEN_HEIGHT // GRID_SIZE

# Movement vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
BG_COLOR = (0, 0, 0)
GRID_BORDER = (93, 216, 228)
APPLE_HUE = (255, 0, 0)
SNAKE_HUE = (0, 255, 0)
SNAKE_HEAD_HUE = (50, 255, 50)  # Slightly different head color for flair

# Game speed
FPS = 20

# Initialize display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


class GameObject:
    """Base class for all in-game entities."""

    def __init__(self, color=(255, 255, 255)):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.color = color

    def draw(self):
        raise NotImplementedError("Subclasses should implement this!")


class Apple(GameObject):
    """Represents the food item."""

    def __init__(self):
        super().__init__(APPLE_HUE)
        self.relocate()

    def relocate(self):
        """Place apple at a random grid-aligned position."""
        x = randint(0, GRID_COLS - 1) * GRID_SIZE
        y = randint(0, GRID_ROWS - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Render the apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, GRID_BORDER, rect, 1)


class Snake(GameObject):
    """Player-controlled snake."""

    def __init__(self):
        super().__init__(SNAKE_HUE)
        self.reset()

    def reset(self):
        """Return snake to start state."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.pending_direction = None
        self.tail = None

    def update_direction(self):
        """Apply queued direction change if valid."""
        if self.pending_direction:
            self.direction = self.pending_direction
            self.pending_direction = None

    def move(self):
        """Advance snake by one step."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction

        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.tail = self.positions.pop()
        else:
            self.tail = None

    def get_head_position(self):
        return self.positions[0]

    def draw(self):
        """Draw all segments, with special head styling."""
        # Draw body
        for pos in self.positions[1:]:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, GRID_BORDER, rect, 1)

        # Draw head
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, SNAKE_HEAD_HUE, head_rect)
        pygame.draw.rect(screen, GRID_BORDER, head_rect, 1)

        # Erase tail if moved
        if self.tail:
            erase_rect = pygame.Rect(self.tail, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BG_COLOR, erase_rect)


def process_input(snake_obj):
    """Handle keyboard events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_obj.direction != DOWN:
                snake_obj.pending_direction = UP
            elif event.key == pygame.K_DOWN and snake_obj.direction != UP:
                snake_obj.pending_direction = DOWN
            elif event.key == pygame.K_LEFT and snake_obj.direction != RIGHT:
                snake_obj.pending_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake_obj.direction != LEFT:
                snake_obj.pending_direction = RIGHT


def main():
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(FPS)
        process_input(snake)
        snake.update_direction()
        snake.move()

        # Apple collision
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.relocate()
            while apple.position in snake.positions:
                apple.relocate()

        # Self-collision
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.relocate()

        # Render frame
        screen.fill(BG_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()