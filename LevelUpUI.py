from Settings import *
from os.path import join

from WindowUI import WindowUI


class LevelUpUI(WindowUI):
    def __init__(self, groups, player):
        super().__init__(groups, player)

        self.background_image = pygame.image.load(join('graphics', 'objects', 'level_up.png')).convert_alpha()

        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.7))

        self.image = pygame.Surface((WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.7), pygame.SRCALPHA)
        self.image.blit(self.background_image, (0, 0))
        self.rect = self.image.get_rect(center=(self.player.rect.centerx, self.player.rect.centery))
        self.bound = ((WINDOW_WIDTH - WINDOW_WIDTH * 0.7) // 2, (WINDOW_HEIGHT - WINDOW_HEIGHT * 0.7) // 2)

    def render(self):
        self.image.blit(self.background_image, (0, 0))
        self.image.blit(self.button_image, self.button_rect)

    def input(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0]:
            relative_mouse_pos = (mouse_pos[0] - 2 * self.button_rect.width, (mouse_pos[1] - self.bound[1]))
            if self.button_rect.collidepoint(relative_mouse_pos):
                self.player.player_data.sound.mouse_click_sound.play()
                self.player.player_data.up_level()
                self.kill()