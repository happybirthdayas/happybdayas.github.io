import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Bird settings
BIRD_WIDTH = 30
BIRD_HEIGHT = 30
BIRD_X = 50
BIRD_Y = SCREEN_HEIGHT // 2
BIRD_GRAVITY = 0.6
BIRD_JUMP = -10

# Pipe settings
PIPE_WIDTH = 50
PIPE_GAP = 150
PIPE_SPEED = 5

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load bird image
bird_img = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_img.fill(RED)

# Load pipe images
pipe_img = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
pipe_img.fill(GREEN)

# Bird class
class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = BIRD_Y
        self.gravity = BIRD_GRAVITY
        self.jump = BIRD_JUMP
        self.velocity = 0

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.jump

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.y))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.y - PIPE_GAP))

    def off_screen(self):
        return self.x < -PIPE_WIDTH

# Game loop
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH)]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Update bird
        bird.update()

        # Update pipes
        for pipe in pipes:
            pipe.update()
            if pipe.off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH))

        # Check collision
        for pipe in pipes:
            if (bird.x + BIRD_WIDTH > pipe.x and
                bird.x < pipe.x + PIPE_WIDTH and
                (bird.y < pipe.y or bird.y + BIRD_HEIGHT > pipe.y + PIPE_GAP)):
                running = False

        # Draw everything
        screen.fill(WHITE)
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()