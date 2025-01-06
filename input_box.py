import pygame

class InputBox:
    
    def __init__(self, image, pos, text=''):
        self.image = image
        self.color = pygame.Color('azure3')
        self.text = text
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.txt_surface = pygame.font.Font("assets/BungeeLayers-Outline.otf", 32).render(text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box
            self.color = pygame.Color('white') if self.active else pygame.Color('azure3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        screen.blit(self.image, self.rect)