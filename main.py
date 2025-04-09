import pygame, mysql.connector, sys, random
from classes import *

pygame.init()
pygame.display.set_caption('Terra Tales')

SCREEN_WIDTH = 1088  #window res
SCREEN_HEIGHT = 612

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

login_bg = pygame.image.load('assets/login_bg.png') #login screen bg
game_bg = pygame.image.load('assets/game_bg.png') #game bg
title = pygame.image.load('assets/TitleRect.png') #title image

#Level Progression Thresholds - Points required to reach each level
level_thresholds = [100, 200, 350, 550, 800, 1100, 1450, 1850, 2300, 2800]

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


def user_auth_menu(registered=False):
    alpha = 0       # 0 = fully transparent, 255 = fully visible
    fade_speed = 0.3          # How fast the message fades out
    hold_duration = 300      # Time (in frames) to stay fully visible before fading
    hold_counter = 0
    success_txt = None

    # Initialize menu buttons
    register_button = Button(base_image1=pygame.image.load("assets/buttons/RegisterRectUp.png"), 
                        pos=(SCREEN_WIDTH//2, 230), 
                        hovering_image1=pygame.image.load("assets/buttons/RegisterRectDown.png"))
    login_button = Button(base_image1=pygame.image.load("assets/buttons/LoginRectUp.png"), 
                        pos=(SCREEN_WIDTH//2, 330), 
                        hovering_image1=pygame.image.load("assets/buttons/LoginRectDown.png"))
    quit_button = Button(base_image1=pygame.image.load("assets/buttons/QuitRectUp.png"), 
                         pos=(SCREEN_WIDTH//2, 430), 
                        hovering_image1=pygame.image.load("assets/buttons/QuitRectDown.png"))
    
    if registered == True:
        success_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf",
                        24).render("Successfully registered!", True, "darkgreen")

    while True:
        # Draw background and title
        screen.blit(login_bg, (0, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))

        # Handle success message fade effect
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

        # Handle button interactions
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

    # Initialize input boxes for registration
    username_box = InputBox(image = pygame.image.load("assets/InputBox.png"),
                        pos=(SCREEN_WIDTH//2, 210), placeholder='Username',
                        screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
    password_box = InputBox(image = pygame.image.load("assets/InputBox.png"),
                        pos=(SCREEN_WIDTH//2, 300), placeholder='Password',
                        screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, hidden=True)
    repeat_password_box = InputBox(image = pygame.image.load("assets/InputBox.png"),
                            pos=(SCREEN_WIDTH//2, 390), placeholder='Repeat Password',
                            screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, hidden=True)

    # Initialize navigation buttons
    proceed_button = Button(base_image1=pygame.image.load("assets/buttons/ProceedRectUp.png"),
                         pos=(SCREEN_WIDTH//2, 500), 
                        hovering_image1=pygame.image.load("assets/buttons/ProceedRectDown.png"))
    home_button = Button(base_image1=pygame.image.load("assets/buttons/HomeRectUp.png"),
                         pos=(70, 70), 
                        hovering_image1=pygame.image.load("assets/buttons/HomeRectDown.png"))

    while True:
        # Draw background and title
        screen.blit(login_bg, (0, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))

        # Handle UI elements
        mouse_pos = pygame.mouse.get_pos()
        input_boxes = [username_box, password_box, repeat_password_box]
        buttons = [home_button, proceed_button]
        
        for button in buttons:
            button.changeImage(mouse_pos)
            button.update(screen)

        for box in input_boxes:
            box.draw(screen)

        # Handle error message fade effect
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
                    # Check for existing usernames
                    db_connect()
                    mycursor.execute("SELECT username FROM users")  #Selects usernames to prevent duplicates
                    usernames = mycursor.fetchall()
                    mycursor.close()
                    mydb.close()

                    # Validate input fields
                    if len(username_box.return_text()) < 1:
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf",
                                        24).render("No username entered!", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 

                    for username in usernames:
                        if username_box.return_text() == username[0]:
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf",
                                        24).render("Username taken!", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 
                    
                    if len(password_box.return_text()) < 8:
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf",
                                        24).render("Password too short! Minimum 8 characters.", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 

                    if password_box.return_text() != repeat_password_box.return_text():
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf",
                                        24).render("Passwords do not match!", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 

                    # If validation passes, create new user
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

    # Initialize input boxes for login
    username_box = InputBox(image = pygame.image.load("assets/InputBox.png"),
                            pos=(SCREEN_WIDTH//2, 210), placeholder='Username', 
                            screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
    password_box = InputBox(image = pygame.image.load("assets/InputBox.png"), 
                            pos=(SCREEN_WIDTH//2, 300), placeholder='Password', 
                            screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, hidden=True)

    # Initialize navigation buttons
    proceed_button = Button(base_image1=pygame.image.load("assets/buttons/ProceedRectUp.png"), 
                            pos=(SCREEN_WIDTH//2, 410), 
                        hovering_image1=pygame.image.load("assets/buttons/ProceedRectDown.png"))
    home_button = Button(base_image1=pygame.image.load("assets/buttons/HomeRectUp.png"), 
                         pos=(70, 70), 
                        hovering_image1=pygame.image.load("assets/buttons/HomeRectDown.png"))
    
    while True:
        # Draw background and title
        screen.blit(login_bg, (0, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))

        # Handle UI elements
        mouse_pos = pygame.mouse.get_pos()
        input_boxes = [username_box, password_box]
        buttons = [home_button, proceed_button]
        
        for button in buttons:
            button.changeImage(mouse_pos)
            button.update(screen)

        for box in input_boxes:
            box.draw(screen)

        # Handle error message fade effect
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
                    # Validate login credentials
                    db_connect()
                    #Selects all user login data for validation
                    mycursor.execute("SELECT username, password FROM users")  
                    user_data = mycursor.fetchall()
                    mycursor.close()
                    mydb.close()

                    for user in user_data:
                        if username_box.return_text() == user[0]\
                              or password_box.return_text() == user[1]:
                            logged_in_user = username_box.return_text()
                            game_menu()
                            break
                        else:
                            invalid_txt = pygame.font.Font("assets/ChangaOne-Regular.ttf", 
                                        24).render("Username or password incorrect!", True, "red")
                            invalid_alpha = 255
                            hold_counter = 0 
        pygame.display.update()


def game_menu():
    # Fetch player stats from database
    db_connect()
    mycursor.execute ("SELECT level FROM users WHERE username = %s", (logged_in_user,))
    level = mycursor.fetchone()
    mycursor.execute("SELECT high_score FROM users WHERE username = %s", (logged_in_user,))
    high_score = mycursor.fetchone()
    mycursor.close()
    mydb.close()

    # Initialize menu buttons
    play_button = Button(base_image1=pygame.image.load("assets/buttons/PlayRectUp.png"), 
                         pos=(SCREEN_WIDTH//2, 250), 
                        hovering_image1=pygame.image.load("assets/buttons/PlayRectDown.png"))
    quit_button = Button(base_image1=pygame.image.load("assets/buttons/QuitRectUp.png"), 
                         pos=(SCREEN_WIDTH//2, 350), 
                        hovering_image1=pygame.image.load("assets/buttons/QuitRectDown.png"))
    sound_button = Button(base_image1=pygame.image.load("assets/buttons/SoundOnRectUp.png"), 
                          pos=(SCREEN_WIDTH//2, 450), 
                        hovering_image1=pygame.image.load("assets/buttons/SoundOnRectDown.png"), 
                        toggle=True,
                        base_image2=pygame.image.load("assets/buttons/SoundOffRectUp.png"),
                        hovering_image2=pygame.image.load("assets/buttons/SoundOffRectDown.png"))

    while True:
        # Draw background and player stats
        screen.blit(login_bg, (0, 0))
        screen.blit(pygame.font.Font("assets/ChangaOne-Regular.ttf", 
                                     28).render(f'Level: {level[0]}', 
                                    True, pygame.Color('white')), (SCREEN_WIDTH-140,27))
        screen.blit(pygame.font.Font("assets/ChangaOne-Regular.ttf", 
                                     28).render(f'High Score: {high_score[0]}', 
                                    True, pygame.Color('white')), (30,27))

        # Handle button interactions
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
                    sound = sound_button.get_state()
                    game()
                
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
                

        pygame.display.update()


def game():
    start_time = pygame.time.get_ticks() #Fetches clock time when game starts for score calculations
    score = 0
    run_count = 0 #Holds the number of times the game loop has run for the first two runs
    current_question = None
    question_timer = 0
    question_interval = 5000  # Show new question every 5 seconds
    game_over = False
    sprite_x = 265  # Default sprite position
    sprite_y = 213  # Default sprite position
    is_walking = False
    target_x = sprite_x
    target_y = sprite_y
    walking_speed = 4  # Speed for horizontal movement
    walking_direction = 1  # 1 for right, -1 for left
    animation_cooldown = 100  # Animation frame timing

    # Get player's level from database
    db_connect()
    mycursor.execute("SELECT level FROM users WHERE username = %s", (logged_in_user,))
    player_level = int(mycursor.fetchone()[0])
    mycursor.close()
    mydb.close()

    # Load questions for current level from questions.txt
    questions = []
    with open('questions.txt', 'r') as file:
        for line in file:
            level, statement, question, left_text, left_health, left_ecology, left_x, left_y, right_text, right_health, right_ecology, right_x, right_y = line.strip().split('|')
            if int(level) == player_level:
                questions.append({
                    "statement": statement,
                    "question": question,
                    "options": {
                        "left": {
                            "text": left_text,
                            "health": int(left_health),
                            "ecology": int(left_ecology),
                            "x": int(left_x),
                            "y": int(left_y)
                        },
                        "right": {
                            "text": right_text,
                            "health": int(right_health),
                            "ecology": int(right_ecology),
                            "x": int(right_x),
                            "y": int(right_y)
                        }
                    }
                })

    # Initialize UI elements
    health_bar = IndicatorBar(SCREEN_WIDTH-208, 30, 200, 25, 100)
    ecology_bar = IndicatorBar(SCREEN_WIDTH-208, 70, 200, 25, 100)

    left_button = Button(base_image1=pygame.image.load("assets/buttons/LeftRectUp.png"), pos=(135, 350), 
                        hovering_image1=pygame.image.load("assets/buttons/LeftRectDown.png"))
    right_button = Button(base_image1=pygame.image.load("assets/buttons/RightRectUp.png"), pos=(SCREEN_WIDTH-130, 350), 
                        hovering_image1=pygame.image.load("assets/buttons/RightRectDown.png"))
    buttons = [left_button, right_button]

    # Load and prepare walking animation
    walking_sprite_sheet_image = pygame.image.load("assets/sprite/walk.png").convert_alpha()
    walking_sprite_sheet = SpriteSheet(walking_sprite_sheet_image)
    
    walking_frames = []
    walking_steps = 10


    for x in range(walking_steps):
        walking_frames.append(walking_sprite_sheet.get_image(x, 128, 128, 1))
    
    idle_sprite_sheet_image = pygame.image.load("assets/sprite/idle.png").convert_alpha()
    idle_sprite_sheet = SpriteSheet(idle_sprite_sheet_image)

    idle_frames = []
    idle_steps = 6

    for x in range(idle_steps):
        idle_frames.append(idle_sprite_sheet.get_image(x, 128, 128, 1))

    frame = 0
    last_animation_update = start_time

    while True:
        current_time = pygame.time.get_ticks()
        # Draw game background and UI
        screen.blit(game_bg, (0, 0))
        screen.blit(pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(f'Score: {score}', True, pygame.Color('white')), (30,27))
        screen.blit(pygame.image.load("assets/heart.png"), (SCREEN_WIDTH-243, 30))
        screen.blit(pygame.image.load("assets/tree.png"), (SCREEN_WIDTH-243, 70))
        
        health_bar.draw(screen)
        ecology_bar.draw(screen)

        # Handle initial animation sequence
        if run_count == 0:
            screen.blit(pygame.image.load("assets/sprite/laying.png"), (370, 300))
            pygame.display.update()
            pygame.time.wait(2000)
            run_count += 1
        elif run_count == 1 and not is_walking:
            current_frame = idle_frames[frame]
            screen.blit(current_frame, (sprite_x, sprite_y))
            if current_time - last_animation_update >= animation_cooldown:
                frame += 1
                if frame >= idle_steps:
                    frame = 0
                last_animation_update = current_time
    

        mouse_pos = pygame.mouse.get_pos() 

        # Update score based on time
        if current_time - start_time - 2500*score >= 2500:
            score += 1

        # Handle health reduction when ecology is depleted
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

            # Check and update high score and total score
            db_connect()
            mycursor.execute("SELECT high_score, total_score FROM users WHERE username = %s", (logged_in_user,))
            high_score, total_score = mycursor.fetchone()
            high_score = int(high_score)
            total_score = int(total_score) if total_score is not None else 0
            
            # Update total score
            total_score = total_score + score
            
            if score > high_score:
                # Update high score
                high_score = score
                
                # Display new high score message
                high_score_font = pygame.font.Font("assets/ChangaOne-Regular.ttf", 32)
                high_score_text = high_score_font.render(f"New High Score: {score}!", True, (255, 215, 0))
                high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
                screen.blit(high_score_text, high_score_rect)
            
            if total_score >= level_thresholds[player_level-1] and player_level < 10:
                # Update level
                player_level += 1

            #Update database with new stats
            mycursor.execute("UPDATE users SET level = %s, high_score = %s, total_score = %s WHERE username = %s", (player_level, high_score, total_score, logged_in_user))
            mydb.commit()
            mycursor.close()
            mydb.close()
            
            # Update the display
            pygame.display.update()
            
            # Wait for 3 seconds before returning to game menu
            pygame.time.wait(3000)
            game_menu()
            return

        # Handle walking animation and movement
        if is_walking:
            # Update animation frame
            if current_time - last_animation_update >= animation_cooldown:
                frame += 1
                last_animation_update = current_time
                if frame >= walking_steps:
                    frame = 0
                
                # Update walking direction based on target
                distance_to_target = abs(sprite_x - target_x)
                if distance_to_target > walking_speed:  # Only move if more than one frame's distance away
                    if sprite_x < target_x:
                        walking_direction = 1
                        sprite_x += walking_speed
                    elif sprite_x > target_x:
                        walking_direction = -1
                        sprite_x -= walking_speed
                else:
                    # Once less than one frame's distance away, snap to exact position and stop walking
                    sprite_x = target_x
                    sprite_y = target_y
                    is_walking = False
                    walking_direction = 1  # Reset direction for next movement
                    frame = 0  # Reset animation frame when stopping

            # Draw walking animation
            current_frame = walking_frames[frame]
            if walking_direction == -1:
                # Flip the sprite horizontally when walking left
                current_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(current_frame, (sprite_x, sprite_y))
            question_timer = current_time

        # Handle question timing - only start after standing up
        if current_time - question_timer >= question_interval and not current_question and questions and not is_walking:
            # Randomly select a question
            current_question = random.choice(questions) 
            question_timer = current_time

        # Draw question and options if active
        if current_question and not is_walking:
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and current_question:
                if left_button.checkForInput(mouse_pos):
                    # Handle left option
                    health_bar.level += current_question["options"]["left"]["health"]
                    ecology_bar.level += current_question["options"]["left"]["ecology"]
                    # Set target coordinates for movement
                    target_x = current_question["options"]["left"]["x"]
                    target_y = current_question["options"]["left"]["y"]
                    is_walking = True
                    questions.remove(current_question)# Remove the used question
                    current_question = None  # Clear current question
                    question_timer = current_time  # Reset timer for next question
                elif right_button.checkForInput(mouse_pos):
                    # Handle right option
                    health_bar.level += current_question["options"]["right"]["health"]
                    ecology_bar.level += current_question["options"]["right"]["ecology"]
                    # Set target coordinates for movement
                    target_x = current_question["options"]["right"]["x"]
                    target_y = current_question["options"]["right"]["y"]
                    is_walking = True
                    questions.remove(current_question)# Remove the used question
                    current_question = None  # Clear current question
                    question_timer = current_time  # Reset timer for next question

        pygame.display.update()


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
        pygame.time.wait(1/frame_rate)

        screen.fill((30,30,30))
        screen.blit(txt_surf, txt_surf_rect)
        pygame.display.flip()

    user_auth_menu()

user_auth_menu()
