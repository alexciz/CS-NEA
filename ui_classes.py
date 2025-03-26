import pygame, time

class InputBox:
    
    def __init__(self, image, pos, placeholder = '', screen_width=0, screen_height=0, hidden=False):
        self.image = image
        self.color = pygame.Color('azure3')
        self.text = ''
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.hidden = hidden
        self.dot_text = ''
        self.screen_width = screen_width
        self.screen_height = screen_height
        if self.hidden == False:
            self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(self.text, True, self.color)
        else:
            self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(self.dot_text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.active = False
        self.placeholder_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(placeholder, True, self.color)
        self.cursor = pygame.Rect(self.rect.topright, (3, self.rect.height-55))        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if not self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = False
            else:
                self.active = True
            # Change the current color of the input box
            self.color = pygame.Color('white') if self.active or self.text != '' else pygame.Color('azure3')
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.dot_text = self.dot_text[:-1]
            else:
                if self.txt_surface.get_width() < self.rect.x - 35:
                    self.text += event.unicode
                    self.dot_text += '·'
             # Re-render the text
        if self.hidden == False:
            self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(self.text, True, self.color)
        else:
            self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 28).render(self.dot_text, True, self.color)

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
    
    def return_text(self):
        input = self.text
        return input
    
class Button():
    def __init__(self, base_image1, pos, hovering_image1, toggle=False, base_image2=None, hovering_image2=None):
        self.base_image1 = base_image1
        self.hovering_image1 = hovering_image1
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.base_image1.get_rect(center=(self.x_pos, self.y_pos))
        self.toggle = toggle
        self.base_image2 = base_image2
        self.hovering_image2 = hovering_image2
        self.state = 0
        self.base_image = base_image1
        self.hovering_image = hovering_image1
        self.image = self.base_image
    def update(self, screen):
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            if self.toggle:
                if self.state == 0:
                    self.base_image = self.base_image2
                    self.hovering_image = self.hovering_image2
                    self.state = 1
                else:
                    self.base_image = self.base_image1
                    self.hovering_image = self.hovering_image1
                    self.state = 0
            return True
        return False

    def changeImage(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.hovering_image
        else:
            self.image = self.base_image


class IndicatorBar():
    def __init__(self, x, y, w, h, max_level):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.level = max_level/2
        self.max_level = max_level

    def draw(self, screen):
        ratio = self.level/self.max_level
        pygame.draw.rect(screen, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, "green", (self.x, self.y, self.w*ratio, self.h))
