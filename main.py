import pygame

#mydb = mysql.connect(
#  host="82.11.62.54",
#  user="client",
#  password="password"
#)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

login_bg = pygame.image.load('login_bg.jpg')

run = True
logged_in = False

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if logged_in == False:
        screen.blit(login_bg, (0, 0))
        pygame.display.update()

pygame.quit()