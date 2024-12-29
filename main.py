import pygame, pygame_gui, mysql.connector

#db connection
mydb = mysql.connector.connect(
  host="82.11.62.54",
  user="client",
  password="password",
  database="user_info"
)

pygame.init()

SCREEN_WIDTH = 800  #window res
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

manager = pygame_gui.UIManager((800, 600))

login_bg = pygame.image.load('login_bg.jpg')

clock = pygame.time.Clock()
run = True
logged_in = False

welcome_text = pygame_gui.elements.UITextBox(
     html_text="<effect id=test>Game Name</effect>",
     relative_rect=pygame.Rect(100, 100, 200, 50))

#game loop
while run:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        manager.process_events(event)

    manager.update(time_delta)

    if logged_in == False:
        screen.blit(login_bg, (0, 0))
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()