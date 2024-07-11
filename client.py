import pygame
import socket
import pickle

# Constants
GRID_SIZE = 10
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SERVER_ADDRESS = '192.168.30.114'
SERVER_PORT = 12345
FPS = 15

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game - Client')

# Initialize clock
clock = pygame.time.Clock()

# Initialize socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Function to send data to the server
def send_data(data):
    try:
        serialized_data = pickle.dumps(data)
        client_socket.sendall(serialized_data)
    except Exception as e:
        print(f"Error sending data: {e}")

# Function to receive data from the server
def receive_data():
    try:
        serialized_data = client_socket.recv(1024)
        data = pickle.loads(serialized_data)
        return data
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None

# Snake class
# Snake class
class Snake:
    def __init__(self, color):
        self.color = color
        self.body = [(0, 0)]  # Initialize with a default position
        self.direction = (0, 0)

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def move(self):
        if len(self.body) > 0:
            head = list(self.body[0])
            new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
            self.body.insert(0, new_head)
            self.body.pop()
        else:
            print("Snake body is empty or invalid.")

# Game loop
def main():
    player_snake = Snake(GREEN)
    opponent_snake = Snake(BLUE)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    player_snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    player_snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player_snake.direction = (1, 0)

        # Move the snake
        player_snake.move()

        # Send player snake position and direction to the server
        send_data({"player_snake": player_snake.body, "player_direction": player_snake.direction})

        # Receive game state from the server
        data = receive_data()
        if data:
            opponent_snake.body = data["opponent_snake"]
            food_position = data["food_position"]

        # Draw everything
        screen.fill(BLACK)
        player_snake.draw(screen)
        opponent_snake.draw(screen)
        pygame.draw.rect(screen, RED, (food_position[0] * GRID_SIZE, food_position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
