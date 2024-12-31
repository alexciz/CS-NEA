import pygame, mysql.connector, time, sys

#db connection
mydb = mysql.connector.connect(
  host="sus.gleeze.com",
  user="client",
  password="password",
  database="user_info"
)

pygame.init()

SCREEN_WIDTH = 800  #window res
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

login_bg = pygame.image.load('login_bg.jpg') #login screen bg

run = True
logged_in = False
clock = pygame.time.Clock()

def welcome_screen():
    frame_rate = 15 #Fade frame rate control
    font_size = 128 #Initial font size
    alpha_rate = 4 #Rate of opacity increase
    x=1 #Exponential constant
    font = pygame.font.Font(None, font_size)
    screen.fill((30,30,30))
    orig_surf = font.render('Game Name', True, 'chartreuse4')
    txt_surf = orig_surf.copy() #This surface is used to adjust the alpha of the txt_surf
    txt_surf_rect = txt_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
    alpha = 0  #The current alpha value of the surface

    while font_size<5800:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        if alpha < 255:
            #Reduce alpha each frame, but make sure it doesn't get below 0
            alpha = min(alpha+alpha_rate, 255)
            txt_surf = orig_surf.copy()  #Fill alpha_surf with this color to set its alpha value
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            alpha_rate += 1
            time.sleep(1/frame_rate)
        else:
            font_size += 16^x
            font = pygame.font.Font(None, font_size)
            txt_surf = font.render('Game Name', True, 'chartreuse4')
            txt_surf_rect = txt_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            x+=1
            

        screen.fill((30,30,30))
        screen.blit(txt_surf, txt_surf_rect)
        pygame.display.flip()
        clock.tick(30)

def login_menu():
    while True:
        screen.blit(login_bg, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        title_text = get_font(100).render('Game Name', True, 'chartreuse4')
        title_rect = MENU_TEXT.get_rect(center=(640, 100))

        register_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        login_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(title_text, title_rect)

        for button in [register_button, login_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if register_button.checkForInput(mouse_pos):
                    
                #if login_button.checkForInput(mouse_pos):
                    
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

welcome_screen()

pygame.quit()
sys.exit()