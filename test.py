import pygame
import mysql.connector
import sys
import random

from button import Button
from input_box import InputBox

# Database connection
mydb = mysql.connector.connect(
    host="sus.gleeze.com",
    user="client",
    password="password",
    database="user_info"
)
mycursor = mydb.cursor()

pygame.init()
pygame.display.set_caption("Terra Tales")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load assets
login_bg = pygame.image.load("assets/login_bg.png")
title = pygame.image.load("assets/TitleRect.png")

# Game variables
logged_in_user = None
player_level = 1
player_high_score = 0
char_health = 100
env_health = 100
score = 0

# Font
font = pygame.font.Font(None, 36)

def fetch_user_data(username):
    """Fetches user level and high score from the database."""
    global player_level, player_high_score
    mycursor.execute("SELECT level, high_score FROM users WHERE username=%s", (username,))
    result = mycursor.fetchone()
    if result:
        player_level, player_high_score = result

def update_user_data(username):
    """Updates user level and high score in the database."""
    mycursor.execute("UPDATE users SET level=%s, high_score=%s WHERE username=%s",
                     (player_level, player_high_score, username))
    mydb.commit()

def game_menu():
    """Displays the game menu after login."""
    global logged_in_user, player_level, player_high_score

    start_button = Button(pygame.image.load("assets/buttons/ProceedRectUp.png"), (SCREEN_WIDTH // 2, 250), pygame.image.load("assets/buttons/ProceedRectUp.png"))
    continue_button = Button(pygame.image.load("assets/buttons/ProceedRectUp.png"), (SCREEN_WIDTH // 2, 350), pygame.image.load("assets/buttons/ProceedRectUp.png"))
    quit_button = Button(pygame.image.load("assets/buttons/QuitRectUp.png"), (SCREEN_WIDTH // 2, 450), pygame.image.load("assets/buttons/ProceedRectUp.png"))

    while True:
        screen.blit(login_bg, (0, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 80)))

        level_text = font.render(f"Level: {player_level}", True, "white")
        high_score_text = font.render(f"High Score: {player_high_score}", True, "white")

        screen.blit(level_text, (20, 20))
        screen.blit(high_score_text, (SCREEN_WIDTH - 180, 20))

        mouse_pos = pygame.mouse.get_pos()
        for button in [start_button, continue_button, quit_button]:
            button.changeImage(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(mouse_pos):
                    game_loop(new_game=True)
                if continue_button.checkForInput(mouse_pos):
                    game_loop(new_game=False)
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game_loop(new_game=True):
    """Main game loop where decisions affect character & environment health."""
    global char_health, env_health, score, player_level, player_high_score

    if new_game:
        char_health = 100
        env_health = 100
        score = 0

    decision1 = Button(pygame.image.load("assets/buttons/QuitRectDown.png"), (SCREEN_WIDTH // 2, 250),(pygame.image.load("assets/buttons/QuitRectDown.png")))
    decision2 = Button(pygame.image.load("assets/buttons/QuitRectUp.png"), (SCREEN_WIDTH // 2, 350),(pygame.image.load("assets/buttons/QuitRectDown.png")))

    running = True
    while running:
        screen.fill((30, 30, 30))

        # Display Health and Score
        health_text = font.render(f"Health: {char_health}%", True, "white")
        env_text = font.render(f"Environment: {env_health}%", True, "white")
        score_text = font.render(f"Score: {score}", True, "white")

        screen.blit(health_text, (20, 20))
        screen.blit(env_text, (20, 60))
        screen.blit(score_text, (SCREEN_WIDTH - 150, 20))

        mouse_pos = pygame.mouse.get_pos()
        for button in [decision1, decision2]:
            button.changeImage(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if decision1.checkForInput(mouse_pos):
                    char_health -= random.randint(5, 15)
                    env_health -= random.randint(5, 15)
                    score += 10
                if decision2.checkForInput(mouse_pos):
                    char_health += random.randint(5, 10)
                    env_health += random.randint(5, 10)
                    score += 15

        # Check for Game Over
        if char_health <= 0 or env_health <= 0:
            game_over()
            running = False

        # Level Up System
        if score > player_high_score:
            player_high_score = score
        if score >= player_level * 50:
            player_level += 1

        pygame.display.update()

def game_over():
    """Handles game over screen and updates the database."""
    global logged_in_user, player_level, player_high_score

    update_user_data(logged_in_user)

    game_over_text = font.render("Game Over!", True, "red")
    restart_button = Button(pygame.image.load("assets/buttons/Restart.png"), (SCREEN_WIDTH // 2, 350))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200)))

        mouse_pos = pygame.mouse.get_pos()
        restart_button.changeImage(mouse_pos)
        restart_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.checkForInput(mouse_pos):
                    game_menu()

        pygame.display.update()

# Entry Point
game_menu()
