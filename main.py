import pygame, mysql.connector, time, sys
from button import Button
from input_box import InputBox

#db connection
mydb = mysql.connector.connect(
  host="sus.gleeze.com",   
  user="client",
  password="password",
  database="user_info"
)
mycursor = mydb.cursor()

pygame.init()

SCREEN_WIDTH = 800  #window res
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

login_bg = pygame.image.load('assets/login_bg.png') #login screen bg
title = pygame.image.load('assets/TitleRect.png')

run = True
logged_in = False
clock = pygame.time.Clock()


def welcome_screen():
    frame_rate = 10 #Fade frame rate control
    font_size = 128 #Font size

    alpha_rate = 5 #Rate of opacity increase
    font = pygame.font.Font(None, font_size)
    screen.fill((30,30,30))
    orig_surf = font.render('Terra Tales', True, 'chartreuse4')
    txt_surf = orig_surf.copy() #This surface is used to adjust the alpha of the txt_surf
    txt_surf_rect = txt_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
    alpha = 0  #The current alpha value of the surface

    while alpha <255 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        #Reduce alpha each frame, but make sure it doesn't get below 0
        alpha = min(alpha+alpha_rate, 255)
        txt_surf = orig_surf.copy()  #Fill alpha_surf with this color to set its alpha value
        alpha_surf.fill((255, 255, 255, alpha))
        txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        alpha_rate += 1
        time.sleep(1/frame_rate)

        screen.fill((30,30,30))
        screen.blit(txt_surf, txt_surf_rect)
        pygame.display.flip()

    user_auth_menu()

def user_auth_menu():
    register_button = Button(base_image=pygame.image.load("assets/buttons/RegisterRectUp.png"), pos=(SCREEN_WIDTH//2, 230), 
                        hovering_image=pygame.image.load("assets/buttons/RegisterRectDown.png"))
        
    login_button = Button(base_image=pygame.image.load("assets/buttons/LoginRectUp.png"), pos=(SCREEN_WIDTH//2, 330), 
                        hovering_image=pygame.image.load("assets/buttons/LoginRectDown.png"))
        
    quit_button = Button(base_image=pygame.image.load("assets/buttons/QuitRectUp.png"), pos=(SCREEN_WIDTH//2, 430), 
                        hovering_image=pygame.image.load("assets/buttons/QuitRectDown.png"))
    while True:
        screen.blit(login_bg, (0, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))

        mouse_pos = pygame.mouse.get_pos()
        buttons = [register_button, login_button, quit_button]

        for button in buttons:
            button.changeImage(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if register_button.checkForInput(mouse_pos):
                    registration_menu()
                if login_button.checkForInput(mouse_pos):
                    login_menu()
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def registration_menu():
    username_box = InputBox(image = pygame.image.load("assets/InputBox.png"), pos=(SCREEN_WIDTH//2, 210), placeholder='Username', screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
    password_box = InputBox(image = pygame.image.load("assets/InputBox.png"), pos=(SCREEN_WIDTH//2, 300), placeholder='Password', screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, hidden=True)
    repeat_password_box = InputBox(image = pygame.image.load("assets/InputBox.png"), pos=(SCREEN_WIDTH//2, 390), placeholder='Repeat Password', screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, hidden=True)

    proceed_button = Button(base_image=pygame.image.load("assets/buttons/ProceedRectUp.png"), pos=(SCREEN_WIDTH//2, 500), 
                        hovering_image=pygame.image.load("assets/buttons/ProceedRectDown.png"))
    home_button = Button(base_image=pygame.image.load("assets/buttons/HomeRectUp.png"), pos=(70, 70), 
                        hovering_image=pygame.image.load("assets/buttons/HomeRectDown.png"))
    

    while True:
        screen.blit(login_bg, (0, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))

        mouse_pos = pygame.mouse.get_pos()
        input_boxes = [username_box, password_box, repeat_password_box]
        buttons = [proceed_button, home_button]
        
        for button in buttons:
            button.changeImage(mouse_pos)
            button.update(screen)

        for box in input_boxes:
            box.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.checkForInput(mouse_pos):
                    user_auth_menu()
                if proceed_button.checkForInput(mouse_pos):
                    if username_box.return_text == mycursor.execute("SELECT username FROM users").fetchall():
                        break
            
        pygame.display.update()

def login_menu():
    time.sleep(0.1)
    pygame.quit

welcome_screen()

