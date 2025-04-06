import pygame, mysql.connector, time, sys, random
from ui_classes import *

pygame.init()
pygame.display.set_caption('Terra Tales')

SCREEN_WIDTH = 1088  #window res
SCREEN_HEIGHT = 612

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

login_bg = pygame.image.load('assets/login_bg.png') #login screen bg
game_bg = pygame.image.load('assets/game_bg.png') #game bg
title = pygame.image.load('assets/TitleRect.png')

clock = pygame.time.Clock()


def db_connect():        #Database Connection
    global mycursor
    global mydb
    mydb = mysql.connector.connect(
    host="sus.gleeze.com",   
    user="client",
    password="password",
    database="user_info"
    )
    mycursor = mydb.cursor()


def welcome_screen():
    frame_rate = 10 #Fade frame rate control
    font_size = 128 #Font size

    alpha_rate = 5 #Rate of opacity increase
    sigma_rate = 0 #Special veriable for darius
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

    register_button = Button(base_image1=pygame.image.load("assets/buttons/RegisterRectUp.png"), pos=(SCREEN_WIDTH//2, 230), 
                        hovering_image1=pygame.image.load("assets/buttons/RegisterRectDown.png"))
        
    login_button = Button(base_image1=pygame.image.load("assets/buttons/LoginRectUp.png"), pos=(SCREEN_WIDTH//2, 330), 
                        hovering_image1=pygame.image.load("assets/buttons/LoginRectDown.png"))
        
    quit_button = Button(base_image1=pygame.image.load("assets/buttons/QuitRectUp.png"), pos=(SCREEN_WIDTH//2, 430), 
                        hovering_image1=pygame.image.load("assets/buttons/QuitRectDown.png"))
    
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

    proceed_button = Button(base_image1=pygame.image.load("assets/buttons/ProceedRectUp.png"), pos=(SCREEN_WIDTH//2, 500), 
                        hovering_image1=pygame.image.load("assets/buttons/ProceedRectDown.png"))
    home_button = Button(base_image1=pygame.image.load("assets/buttons/HomeRectUp.png"), pos=(70, 70), 
                        hovering_image1=pygame.image.load("assets/buttons/HomeRectDown.png"))


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
                    db_connect()
                    mycursor.execute("SELECT username FROM users")  #Selects usernames to prevent duplicates
                    usernames = mycursor.fetchall()
                    mycursor.close()
                    mydb.close()

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
                        db_connect()
                        sql = "INSERT INTO users (username, password, level, high_score) VALUES (%s, %s, 1, 0)"
                        val = (username_box.return_text(), password_box.return_text())
                        mycursor.execute(sql, val)
                        mydb.commit()
                        mycursor.close()
                        mydb.close()
                        user_auth_menu(True)

        pygame.display.update()


def login_menu():
    invalid_alpha = 0       # 0 = fully transparent, 255 = fully visible
    fade_speed = 0.3          # How fast the message fades out
    hold_duration = 300      # Time (in frames) to stay fully visible before fading
    hold_counter = 0
    invalid_txt = None
    global logged_in_user

    username_box = InputBox(image = pygame.image.load("assets/InputBox.png"), pos=(SCREEN_WIDTH//2, 210), placeholder='Username', screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
    password_box = InputBox(image = pygame.image.load("assets/InputBox.png"), pos=(SCREEN_WIDTH//2, 300), placeholder='Password', screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, hidden=True)

    proceed_button = Button(base_image1=pygame.image.load("assets/buttons/ProceedRectUp.png"), pos=(SCREEN_WIDTH//2, 410), 
                        hovering_image1=pygame.image.load("assets/buttons/ProceedRectDown.png"))
    home_button = Button(base_image1=pygame.image.load("assets/buttons/HomeRectUp.png"), pos=(70, 70), 
                        hovering_image1=pygame.image.load("assets/buttons/HomeRectDown.png"))
    
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
                    db_connect()
                    mycursor.execute("SELECT username, password FROM users")  #Selects all user login data for validation
                    user_data = mycursor.fetchall()
                    mycursor.close()
                    mydb.close()

                    for user in user_data:
                        print(user)
                        if username_box.return_text() == user[0] or password_box.return_text() == user[1]:
                            logged_in_user = username_box.return_text()
                            game_menu()
                            break
                        else:
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf", 24).render("Username or password incorrect!", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 
        pygame.display.update()


def game_menu():
    global sound
    sound = True
    db_connect()
    mycursor.execute ("SELECT level FROM users WHERE username = %s", (logged_in_user,))
    level = mycursor.fetchone()
    mycursor.execute("SELECT high_score FROM users WHERE username = %s", (logged_in_user,))
    high_score = mycursor.fetchone()
    mycursor.close()
    mydb.close()

    play_button = Button(base_image1=pygame.image.load("assets/buttons/PlayRectUp.png"), pos=(SCREEN_WIDTH//2, 250), 
                        hovering_image1=pygame.image.load("assets/buttons/PlayRectDown.png"))
    quit_button = Button(base_image1=pygame.image.load("assets/buttons/QuitRectUp.png"), pos=(SCREEN_WIDTH//2, 350), 
                        hovering_image1=pygame.image.load("assets/buttons/QuitRectDown.png"))
    sound_button = Button(base_image1=pygame.image.load("assets/buttons/SoundOnRectUp.png"), pos=(SCREEN_WIDTH//2, 450), 
                        hovering_image1=pygame.image.load("assets/buttons/SoundOnRectDown.png"), toggle=True,
                        base_image2=pygame.image.load("assets/buttons/SoundOffRectUp.png"),
                        hovering_image2=pygame.image.load("assets/buttons/SoundOffRectDown.png"))

    while True:
        screen.blit(login_bg, (0, 0))
        screen.blit(pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(f'Level: {level[0]}', True, pygame.Color('white')), (SCREEN_WIDTH-140,27))
        screen.blit(pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(f'High Score: {high_score[0]}', True, pygame.Color('white')), (30,27))

        mouse_pos = pygame.mouse.get_pos() 
        buttons = [play_button, quit_button, sound_button]

        for button in buttons:
            button.changeImage(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_pos):
                    game(logged_in_user)
                
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
                
                if sound_button.checkForInput(mouse_pos):
                    if sound:
                        sound = False
                    else:
                        sound = True

        pygame.display.update()


def game(user):
    logged_in_user = "test"
    start_time = pygame.time.get_ticks() #Fetches clock time when game starts for score calculations
    score = 0
    sprite_state = 1  # 1 for laying, 2 for standing
    current_question = None
    question_timer = 0
    question_interval = 5000  # Show new question every 5 seconds
    game_over = False

    # Get player's level
    db_connect()
    mycursor.execute("SELECT level FROM users WHERE username = %s", (logged_in_user,))
    player_level = mycursor.fetchone()[0]
    mycursor.close()
    mydb.close()

    # Load questions for current level
    questions = []
    with open('questions.txt', 'r') as file:
        for line in file:
            level, statement, question, left_text, left_health, left_ecology, right_text, right_health, right_ecology = line.strip().split('|')
            if int(level) == int(player_level):
                questions.append({
                    "statement": statement,
                    "question": question,
                    "options": {
                        "left": {
                            "text": left_text,
                            "health": int(left_health),
                            "ecology": int(left_ecology)
                        },
                        "right": {
                            "text": right_text,
                            "health": int(right_health),
                            "ecology": int(right_ecology)
                        }
                    }
                })

    health_bar = IndicatorBar(SCREEN_WIDTH-208, 30, 200, 25, 100)
    ecology_bar = IndicatorBar(SCREEN_WIDTH-208, 70, 200, 25, 100)

    left_button = Button(base_image1=pygame.image.load("assets/buttons/LeftRectUp.png"), pos=(135, 350), 
                        hovering_image1=pygame.image.load("assets/buttons/LeftRectDown.png"))
    right_button = Button(base_image1=pygame.image.load("assets/buttons/RightRectUp.png"), pos=(SCREEN_WIDTH-130, 350), 
                        hovering_image1=pygame.image.load("assets/buttons/RightRectDown.png"))
    buttons = [left_button, right_button]

    while True:
        screen.blit(game_bg, (0, 0))
        screen.blit(pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(f'Score: {score}', True, pygame.Color('white')), (30,27))
        screen.blit(pygame.image.load("assets/heart.png"), (SCREEN_WIDTH-243, 30))
        screen.blit(pygame.image.load("assets/tree.png"), (SCREEN_WIDTH-243, 70))
        
        mouse_pos = pygame.mouse.get_pos() 

        if pygame.time.get_ticks() - start_time - 2500*score >= 2500:
            score += 1
    
        health_bar.draw(screen)
        ecology_bar.draw(screen)

        # Decrease health when ecology is 0
        if ecology_bar.level <= 0:
            health_bar.level = max(0, health_bar.level - 0.004)  # Decrease health by 1, but don't go below 0

        # Check for game over condition
        if health_bar.level <= 0 and not game_over:
            game_over = True
            # Create a semi-transparent black overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            screen.blit(overlay, (0, 0))
            
            # Create and display game over text
            game_over_font = pygame.font.Font("assets/ChangaOne-Regular.ttf", 64)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, text_rect)

            # Check and update high score
            db_connect()
            mycursor.execute("SELECT high_score FROM users WHERE username = %s", (logged_in_user,))
            current_high_score = mycursor.fetchone()[0]
            
            if score > current_high_score:
                # Update high score in database
                mycursor.execute("UPDATE users SET high_score = %s WHERE username = %s", (score, logged_in_user))
                mydb.commit()
                
                # Display new high score message
                high_score_font = pygame.font.Font("assets/ChangaOne-Regular.ttf", 32)
                high_score_text = high_score_font.render(f"New High Score: {score}!", True, (255, 215, 0))
                high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
                screen.blit(high_score_text, high_score_rect)
                pygame.display.update()
            
            mycursor.close()
            mydb.close()
            
            # Wait for 3 seconds before returning to game menu
            pygame.time.wait(3000)
            game_menu()
            return

        # Handle laying to standing animation
        if sprite_state == 1 and pygame.time.get_ticks() - start_time >= 2000:
            sprite_state = 2
            question_timer = pygame.time.get_ticks()  # Reset timer when sprite stands up

        # Handle question timing - only start after standing up
        current_time = pygame.time.get_ticks()
        if sprite_state == 2 and current_time - question_timer >= question_interval and not current_question and questions:
            # Randomly select a question
            current_question = random.choice(questions) 
            question_timer = current_time

        # Draw question and options if active
        if current_question:
            # Draw question text
            question_font = pygame.font.Font("assets/ChangaOne-Regular.ttf", 32)
            statement_text = question_font.render(current_question["statement"], True, "black")
            screen.blit(statement_text, statement_text.get_rect(center=(SCREEN_WIDTH//2, 70)))
            question_text = question_font.render(current_question["question"], True, "black")
            screen.blit(question_text, question_text.get_rect(center=(SCREEN_WIDTH//2, 100)))

            # Draw option texts
            left_text = question_font.render(current_question["options"]["left"]["text"], True, "black")
            right_text = question_font.render(current_question["options"]["right"]["text"], True, "black")
            screen.blit(left_text, left_text.get_rect(center=(135, 240)))
            screen.blit(right_text, right_text.get_rect(center=(SCREEN_WIDTH-130, 240)))

            # Show decision buttons
            for button in buttons:
                button.changeImage(mouse_pos)
                button.update(screen)

        # Draw the appropriate sprite
        if sprite_state == 1:
            screen.blit(pygame.image.load("assets/sprite/laying.png"), (370, 300))
        elif sprite_state == 2:
            screen.blit(pygame.image.load("assets/sprite/standing.png"), (320, 273))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and current_question:
                if left_button.checkForInput(mouse_pos):
                    # Handle left option
                    health_bar.level += current_question["options"]["left"]["health"]
                    ecology_bar.level += current_question["options"]["left"]["ecology"]
                    current_question = None  # Clear current question
                    questions.pop(0)  # Remove the used question
                    question_timer = pygame.time.get_ticks()  # Reset timer for next question
                elif right_button.checkForInput(mouse_pos):
                    # Handle right option
                    health_bar.level += current_question["options"]["right"]["health"]
                    ecology_bar.level += current_question["options"]["right"]["ecology"]
                    current_question = None  # Clear current question
                    questions.pop(0)  # Remove the used question
                    question_timer = pygame.time.get_ticks()  # Reset timer for next question


        pygame.display.update()


game()
