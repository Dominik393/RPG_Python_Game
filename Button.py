import pygame.font
from Settings import *

class Button:
    def __init__(self, x, y, width, height, text=None, color=(73, 73, 73), highlight_color=(189, 189, 189),
                 function=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.highlight_color = highlight_color
        self.function = function
        self.surface = pygame.Surface((self.width, self.height))
        self.is_surface = False


    def set_surface(self, surface):
        self.surface = surface
        self.is_surface = True

    def draw(self, win, outline=None):
        if self.is_surface:
            win.blit(self.surface, (self.x, self.y))
            return

        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text:
            font = pygame.font.Font(None, 44)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2) + 3))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def use_function(self, *args):
        if self.function:
            self.function(*args)
