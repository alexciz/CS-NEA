import pygame, time

class InputBox:
    
    def __init__(self, image, pos, placeholder = '', screen_width = 0, screen_height= 0):
        self.image = image
        self.color = pygame.Color('azure2')
        self.text = ''
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.active = False
        self.placeholder_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(placeholder, True, self.color)
        self.cursor = pygame.Rect(self.rect.topright, (3, self.rect.height-55))        

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if not self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = False
            else:
                self.active = True
            # Change the current color of the input box
            self.color = pygame.Color('white') if self.active else pygame.Color('azure3')
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if self.txt_surface.get_width() > self.rect.x - 35:
                    limit_text = pygame.font.Font("assets/ChangaOne-Regular.ttf", 16).render("Character Limit Reached", True, color='red')
                    screen.blit(limit_text,(100,100))
                    print("print")
                else:
                    self.text += event.unicode
             # Re-render the text
            self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the rect.
        screen.blit(self.image, self.rect)
        # Blit the text.
        if self.text == '' and self.active == False:
            screen.blit(self.placeholder_surface, (self.rect.x+12 , self.rect.y+25))
        else:
            screen.blit(self.txt_surface, (self.rect.x+12 , self.rect.y+25))
        if self.active:
            if time.time() % 1 > 0.5:
                text_rect = self.txt_surface.get_rect(topleft = (self.rect.x + 12, self.rect.y + 26))
                self.cursor.midleft = text_rect.midright
                pygame.draw.rect(screen, self.color, self.cursor)

