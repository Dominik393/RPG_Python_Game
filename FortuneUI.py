from Settings import *
from WindowUI import WindowUI


class FortuneUI(WindowUI):
    def __init__(self, groups, player, fortune, message, item_icon=None):
        super().__init__(groups, player)
        self.fortune = fortune
        self.message = message
        self.item_icon = item_icon

        self.image.fill('white')
        self.rect = self.image.get_rect(center=(self.player.rect.centerx, self.player.rect.centery))
        self.bound = ((WINDOW_WIDTH - WINDOW_WIDTH * 0.7) // 2, (WINDOW_HEIGHT - WINDOW_HEIGHT * 0.7) // 2)

        self.item_rect = None

    def render(self):
        self.image.fill('white')

        if self.item_icon:
            self.item_rect = self.item_icon.get_rect(
                center=(self.image.get_width() // 2, self.image.get_height() - self.image.get_height() // 3))
            self.image.blit(self.item_icon, self.item_rect)

        text_surface = self.font.render(self.message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
        self.image.blit(text_surface, text_rect)

        self.image.blit(self.button_image, self.button_rect)