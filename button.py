class Button():
    def __init__(self, base_image, pos, hovering_image):
        self.base_image = base_image
        self.hovering_image = hovering_image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.base_image.get_rect(center=(self.x_pos, self.y_pos))
        self.image = self.base_image
        
    def update(self, screen):
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeImage(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.hovering_image
        else:
            self.image = self.base_image