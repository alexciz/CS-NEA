import pygame, time

class InputBox:
    # A class to handle text input boxes with placeholder text and password masking
    def __init__(self, image, pos, placeholder = '', screen_width=0,
                 screen_height=0, hidden=False):
        # Initialize input box properties
        self.image = image
        self.color = pygame.Color('azure3')
        self.text = ''
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.hidden = hidden
        self.dot_text = ''
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Set up text rendering based on visibility
        if self.hidden == False:
            self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf",
                                    28).render(self.text, True, self.color)
        else:
            self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf",
                                    28).render(self.dot_text, True, self.color)
        # Set up box positioning and cursor
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.active = False
        self.placeholder_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 
                                    28).render(placeholder, True, self.color)
        self.cursor = pygame.Rect(self.rect.topright, (3, self.rect.height-55))        

    def handle_event(self, event):
        # Handle mouse and keyboard events for the input box
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle box activation/deactivation on click
            if not self.rect.collidepoint(event.pos):
                self.active = False
            else:
                self.active = True
            # Update box color based on state
            self.color = pygame.Color('white') if self.active\
                 or self.text != '' else pygame.Color('azure3')
        if event.type == pygame.KEYDOWN and self.active:
            # Handle text input and backspace
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.dot_text = self.dot_text[:-1]
            else:
                if self.txt_surface.get_width() < self.rect.x - 35:
                    self.text += event.unicode
                    self.dot_text += '·'
            # Update text rendering
            if self.hidden == False:
                self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf",
                                    28).render(self.text, True, self.color)
            else:
                self.txt_surface = pygame.font.Font("assets/ChangaOne-Regular.ttf", 
                                    28).render(self.dot_text, True, self.color)

    def draw(self, screen):
        # Draw the input box, text, and cursor
        # Draw the box background
        screen.blit(self.image, self.rect)
        # Draw placeholder or input text
        if self.text == '' and self.active == False:
            screen.blit(self.placeholder_surface, (self.rect.x+12 , self.rect.y+25))
        else:
            screen.blit(self.txt_surface, (self.rect.x+12 , self.rect.y+25))
        # Draw blinking cursor when active
        if self.active:
            if time.time() % 1 > 0.5:
                text_rect = self.txt_surface.get_rect(topleft = (self.rect.x + 12,
                                                                 self.rect.y + 26))
                self.cursor.midleft = text_rect.midright
                pygame.draw.rect(screen, self.color, self.cursor)
    
    def return_text(self):
        # Return the current text in the input box
        input = self.text
        return input
    
class Button():
    # A class to handle interactive buttons with hover effects and toggle states
    def __init__(self, base_image1, pos, hovering_image1, toggle=False,
                  base_image2=None, hovering_image2=None):
        # Initialize button images and position
        self.base_image1 = base_image1
        self.hovering_image1 = hovering_image1
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.base_image1.get_rect(center=(self.x_pos, self.y_pos))
        # Set up toggle functionality
        self.toggle = toggle
        self.base_image2 = base_image2
        self.hovering_image2 = hovering_image2
        self.state = 0
        self.base_image = base_image1
        self.hovering_image = hovering_image1
        self.image = self.base_image

    def update(self, screen):
        # Draw the button on the screen
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        # Check if the button was clicked and handle toggle state
        if position[0] in range(self.rect.left, self.rect.right)\
            and position[1] in range(self.rect.top, self.rect.bottom):
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
        # Change button image based on hover state
        if position[0] in range(self.rect.left, self.rect.right)\
            and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.hovering_image
        else:
            self.image = self.base_image

    def get_state(self):
        # Return the current state of the button
        toggle_state = self.state
        return toggle_state


class IndicatorBar():
    # A class to handle progress/status bars with visual feedback
    def __init__(self, x, y, w, h, max_level):
        # Initialize bar properties
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.level = max_level/2
        self.max_level = max_level

    def draw(self, screen):
        # Draw the indicator bar with current level
        ratio = self.level/self.max_level
        pygame.draw.rect(screen, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, "green", (self.x, self.y, self.w*ratio, self.h))

class SpriteSheet():
    # A class to handle sprite sheet animations
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, frame, width, height, scale):
        # Extract and scale a single frame from the sprite sheet
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((0,0,0))
        
        return image


class Button1():
    # A class to handle interactive buttons with hover effects
    def __init__(self, base_image, pos, hovering_image):
        # Initialize button properties
        self.base_image = base_image
        self.hovering_image = hovering_image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.base_image.get_rect(center=(self.x_pos, self.y_pos))
        self.image = self.base_image
        
    def update(self, screen):
        # Draw the button on the screen
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        # Check if the button was clicked
        if position[0] in range(self.rect.left, self.rect.right)\
            and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeImage(self, position):
        # Change button image based on hover state
        if position[0] in range(self.rect.left, self.rect.right)\
            and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.hovering_image
        else:
            self.image = self.base_image

    
