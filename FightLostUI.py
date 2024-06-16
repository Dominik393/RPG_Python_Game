from Settings import *
from WindowUI import WindowUI


class FightLostUI(WindowUI):
    def __init__(self, groups, player):
        super().__init__(groups, player)
        self.message = "You lost this battle. Wait a while for your strength to recover to continue."
        self.item_icon = pygame.image.load(join('graphics', 'objects', 'health.png')).convert_alpha()

        self.image.fill('white')
        self.rect = self.image.get_rect(center=(self.player.rect.centerx, self.player.rect.centery))
        self.bound = ((WINDOW_WIDTH - WINDOW_WIDTH * 0.7) // 2, (WINDOW_HEIGHT - WINDOW_HEIGHT * 0.7) // 2)

    def render(self):
        self.image.fill('white')

        item_rect = self.item_icon.get_rect(
            center=(self.image.get_width() // 2, self.image.get_height() - self.image.get_height() // 3))
        self.image.blit(self.item_icon, item_rect)

        text_surface = self.font.render(self.message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2 - 20))
        self.image.blit(text_surface, text_rect)

        # Adding the red text below the main message
        attention_message = "Attention! If you have at least 10% health, enemies will attack you!"
        attention_surface = self.font.render(attention_message, True, (255, 0, 0))
        attention_rect = attention_surface.get_rect(
            center=(self.image.get_width() // 2, self.image.get_height() // 2 + 30))
        self.image.blit(attention_surface, attention_rect)

        self.image.blit(self.button_image, self.button_rect)
