class Button():
    def __init__(self, base_image1, pos, hovering_image1, toggle = False, base_image2=None, hovering_image2=None):
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