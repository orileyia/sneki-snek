import pygame
import time
import random
import json

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Define screen size
screen_width = 600
screen_height = 400

# Set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Sneki-Snek')

# Colors
black = pygame.Color('black')
white = pygame.Color('white')
red = pygame.Color('red')
green = pygame.Color('green')
blue = pygame.Color('blue')

# Clock
clock = pygame.time.Clock()

# Load audio files
pygame.mixer.music.load('background.mp3')
eat_sound = pygame.mixer.Sound('eat_sound.wav')

# Play background music
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Initialize game variables
def init_game():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (screen_width // 10)) * 10,
                random.randrange(1, (screen_height // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

# Save leaderboard to a file
def save_leaderboard(leaderboard):
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboard, f)

# Load leaderboard from a file
def load_leaderboard():
    try:
        with open('leaderboard.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Add a new score to the leaderboard
def add_to_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]  # Keep top 10 scores
    save_leaderboard(leaderboard)

# Display the leaderboard
def show_leaderboard():
    leaderboard = load_leaderboard()
    screen.fill(black)
    font = pygame.font.SysFont('Consolas', 50)
    title_surface = font.render('Leaderboard', True, white)
    title_rect = title_surface.get_rect()
    title_rect.midtop = (screen_width / 2, 50)
    screen.blit(title_surface, title_rect)
    
    font = pygame.font.SysFont('Consolas', 30)
    for i, entry in enumerate(leaderboard):
        entry_surface = font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, white)
        entry_rect = entry_surface.get_rect()
        entry_rect.midtop = (screen_width / 2, 100 + i * 30)
        screen.blit(entry_surface, entry_rect)

    # Instruction text
    instruction_font = pygame.font.SysFont('Consolas', 20)
    instruction_text = instruction_font.render('Press Enter to go back to menu', True, white)
    instruction_rect = instruction_text.get_rect()
    instruction_rect.midbottom = (screen_width / 2, screen_height - 20)
    screen.blit(instruction_text, instruction_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    main_menu()

# Main menu
def main_menu():
    screen.fill(black)
    font = pygame.font.SysFont('Consolas', 50)
    title_surface = font.render('Snake Game', True, white)
    title_rect = title_surface.get_rect()
    title_rect.midtop = (screen_width / 2, screen_height / 4)
    screen.blit(title_surface, title_rect)
    
    button_font = pygame.font.SysFont('Consolas', 30)
    start_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 - 25, 200, 50)
    leaderboard_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 50, 200, 50)
    pygame.draw.rect(screen, blue, start_button)
    pygame.draw.rect(screen, blue, leaderboard_button)
    
    start_text = button_font.render('Start Game', True, white)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)
    
    leaderboard_text = button_font.render('Leaderboard', True, white)
    leaderboard_text_rect = leaderboard_text.get_rect(center=leaderboard_button.center)
    screen.blit(leaderboard_text, leaderboard_text_rect)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    ask_player_name()
                    return
                if leaderboard_button.collidepoint(event.pos):
                    show_leaderboard()
                    return

# Ask player name
def ask_player_name():
    global player_name
    player_name = ""
    input_active = True
    
    while input_active:
        screen.fill(black)
        font = pygame.font.SysFont('Consolas', 50)
        prompt_surface = font.render('Enter Name:', True, white)
        prompt_rect = prompt_surface.get_rect()
        prompt_rect.midtop = (screen_width / 2, screen_height / 4)
        screen.blit(prompt_surface, prompt_rect)
        
        name_surface = font.render(player_name, True, white)
        name_rect = name_surface.get_rect()
        name_rect.midtop = (screen_width / 2, screen_height / 2)
        screen.blit(name_surface, name_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(player_name) == 3:
                        input_active = False
                        init_game()
                        return
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 3 and event.unicode.isalpha():
                    player_name += event.unicode.upper()

# Game Over function with Restart and Menu buttons
def game_over():
    add_to_leaderboard(player_name, score)
    font = pygame.font.SysFont('Consolas', 50)
    game_over_surface = font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width / 2, screen_height / 4)
    screen.fill(black)
    screen.blit(game_over_surface, game_over_rect)

    button_font = pygame.font.SysFont('Consolas', 30)
    restart_button = pygame.Rect(screen_width / 2 - 75, screen_height / 2 - 25, 150, 50)
    menu_button = pygame.Rect(screen_width / 2 - 75, screen_height / 2 + 50, 150, 50)
    pygame.draw.rect(screen, blue, restart_button)
    pygame.draw.rect(screen, blue, menu_button)
    
    restart_text = button_font.render('Restart', True, white)
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)
    
    menu_text = button_font.render('Menu', True, white)
    menu_text_rect = menu_text.get_rect(center=menu_button.center)
    screen.blit(menu_text, menu_text_rect)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    pygame.mixer.music.play(-1)
                    init_game()
                    return
                if menu_button.collidepoint(event.pos):
                    main_menu()
                    return

# Initialize game variables for the first time
main_menu()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Validate the direction change
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 10
        food_spawn = False
        eat_sound.play()  # Play the eating sound
    else:
        snake_body.pop()

    # Spawn new food
    if not food_spawn:
        food_pos = [random.randrange(1, (screen_width // 10)) * 10,
                    random.randrange(1, (screen_height // 10)) * 10]
    food_spawn = True

    # Game over conditions
    if snake_pos[0] < 0 or snake_pos[0] > screen_width - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > screen_height - 10:
        game_over()
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Draw everything
    screen.fill(black)
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Display score
    font = pygame.font.SysFont('Consolas', 35)
    score_surface = font.render('Score : ' + str(score), True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (screen_width / 2, 15)
    screen.blit(score_surface, score_rect)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second / Refresh Rate
    clock.tick(20)

pygame.quit()
quit()
