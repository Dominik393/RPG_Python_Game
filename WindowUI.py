from Settings import *
from os.path import join


class WindowUI(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.font = pygame.font.Font(None, 36)

        self.image = pygame.Surface((WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.7))

        self.button_font = pygame.font.Font(None, 24)
        self.button_text = self.button_font.render('Close', True, (255, 255, 255))
        self.button_image = pygame.Surface((100, 50))
        self.button_image.fill((0, 0, 0))

        button_text_rect = self.button_text.get_rect(center=(self.button_image.get_width() // 2, self.button_image.get_height() // 2))
        self.button_image.blit(self.button_text, button_text_rect.topleft)

        self.button_rect = self.button_image.get_rect(
            center=(self.image.get_width() // 2, self.image.get_height() - 30))

    def render(self):
        raise NotImplementedError

    def update(self, dt):
        self.input()
        self.rect.center = (self.player.rect.centerx, self.player.rect.centery)
        self.render()

    def input(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0]:
            relative_mouse_pos = (mouse_pos[0] - 2 * self.button_rect.width, (mouse_pos[1] - self.bound[1]))
            if self.button_rect.collidepoint(relative_mouse_pos):
                self.player.player_data.sound.mouse_click_sound.play()
                self.kill()