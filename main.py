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
pygame.display.set_caption('Terra Tales')

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

def user_auth_menu(registered=False):
    alpha = 0       # 0 = fully transparent, 255 = fully visible
    fade_speed = 0.3          # How fast the message fades out
    hold_duration = 300      # Time (in frames) to stay fully visible before fading
    hold_counter = 0
    success_txt = None

    register_button = Button(base_image=pygame.image.load("assets/buttons/RegisterRectUp.png"), pos=(SCREEN_WIDTH//2, 230), 
                        hovering_image=pygame.image.load("assets/buttons/RegisterRectDown.png"))
        
    login_button = Button(base_image=pygame.image.load("assets/buttons/LoginRectUp.png"), pos=(SCREEN_WIDTH//2, 330), 
                        hovering_image=pygame.image.load("assets/buttons/LoginRectDown.png"))
        
    quit_button = Button(base_image=pygame.image.load("assets/buttons/QuitRectUp.png"), pos=(SCREEN_WIDTH//2, 430), 
                        hovering_image=pygame.image.load("assets/buttons/QuitRectDown.png"))
    
    if registered == True:
        success_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf", 24).render("Successfully registered!", True, "darkgreen")

    while True:
        screen.blit(login_bg, (0, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))

        if success_txt is not None:
            if hold_counter < hold_duration:
                # Keep message fully visible during "hold" phase
                hold_counter += 1
                alpha = 255
            else:
                # Fade out after hold duration
                alpha = max(alpha - fade_speed, 0)

            # Draw the message with current alpha
            success_txt.set_alpha(alpha)
            screen.blit(success_txt, success_txt.get_rect(center=(SCREEN_WIDTH//2, 500)))
            if alpha <= 0:
                success_txt = None

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
    invalid_alpha = 0       # 0 = fully transparent, 255 = fully visible
    fade_speed = 0.3          # How fast the message fades out
    hold_duration = 300      # Time (in frames) to stay fully visible before fading
    hold_counter = 0
    invalid_txt = None

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
        buttons = [home_button, proceed_button]
        
        for button in buttons:
            button.changeImage(mouse_pos)
            button.update(screen)

        for box in input_boxes:
            box.draw(screen)

        if invalid_txt is not None:
            if hold_counter < hold_duration:
                # Keep message fully visible during "hold" phase
                hold_counter += 1
                invalid_alpha = 255
            else:
                # Fade out after hold duration
                invalid_alpha = max(invalid_alpha - fade_speed, 0)

            # Draw the message with current alpha
            invalid_txt.set_alpha(invalid_alpha)
            screen.blit(invalid_txt, invalid_txt.get_rect(center=(SCREEN_WIDTH//2, 565)))

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
                    invalid_txt = None
                    mycursor.execute("SELECT username FROM users")  #Selects usernames to prevent duplicates
                    usernames = mycursor.fetchall()

                    if len(username_box.return_text()) < 1:
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf", 24).render("No username entered!", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 

                    for username in usernames:
                        if username_box.return_text() == username[0]:
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf", 24).render("Username taken!", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 
                    
                    if len(password_box.return_text()) < 8:
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf", 24).render("Password too short! Minimum 8 characters.", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 

                    if password_box.return_text() != repeat_password_box.return_text():
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf", 24).render("Passwords do not match!", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 

                    if invalid_txt == None:
                        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                        val = (username_box.return_text(), password_box.return_text())
                        mycursor.execute(sql, val)
                        user_auth_menu(True)

        pygame.display.update()

def login_menu():
    invalid_alpha = 0       # 0 = fully transparent, 255 = fully visible
    fade_speed = 0.3          # How fast the message fades out
    hold_duration = 300      # Time (in frames) to stay fully visible before fading
    hold_counter = 0
    invalid_txt = None

    username_box = InputBox(image = pygame.image.load("assets/InputBox.png"), pos=(SCREEN_WIDTH//2, 210), placeholder='Username', screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
    password_box = InputBox(image = pygame.image.load("assets/InputBox.png"), pos=(SCREEN_WIDTH//2, 300), placeholder='Password', screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, hidden=True)

    proceed_button = Button(base_image=pygame.image.load("assets/buttons/ProceedRectUp.png"), pos=(SCREEN_WIDTH//2, 410), 
                        hovering_image=pygame.image.load("assets/buttons/ProceedRectDown.png"))
    home_button = Button(base_image=pygame.image.load("assets/buttons/HomeRectUp.png"), pos=(70, 70), 
                        hovering_image=pygame.image.load("assets/buttons/HomeRectDown.png"))
    
    while True:
        screen.blit(login_bg, (0, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))

        mouse_pos = pygame.mouse.get_pos()
        input_boxes = [username_box, password_box]
        buttons = [home_button, proceed_button]
        
        for button in buttons:
            button.changeImage(mouse_pos)
            button.update(screen)

        for box in input_boxes:
            box.draw(screen)

        if invalid_txt is not None:
            if hold_counter < hold_duration:
                # Keep message fully visible during "hold" phase
                hold_counter += 1
                invalid_alpha = 255
            else:
                # Fade out after hold duration
                invalid_alpha = max(invalid_alpha - fade_speed, 0)

            # Draw the message with current alpha
            invalid_txt.set_alpha(invalid_alpha)
            screen.blit(invalid_txt, invalid_txt.get_rect(center=(SCREEN_WIDTH//2, 500)))

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
                    invalid_txt = None
                    mycursor.execute("SELECT * FROM users")  #Selects all user login data for validation
                    user_data = mycursor.fetchall()

                    for user in user_data:
                        if username_box.return_text() != user[0] or password_box.return_text() != user[1]:
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf", 24).render("Username or password incorrect!", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 

                    if invalid_txt == None:
                        game_menu()

        pygame.display.update()


def game_menu():
    time.sleep(5)
    pygame.quit()
    sys.exit()

welcome_screen()

