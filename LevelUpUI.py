from Settings import *
from os.path import join


class LevelUpUI(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.font = pygame.font.Font(None, 36)

        # Завантажуємо зображення фону
        self.background_image = pygame.image.load(join('graphics', 'objects', 'level_up.png')).convert_alpha()

        # Змінюємо розмір зображення фону під розмір вікна
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.7))

        self.image = pygame.Surface((WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.7), pygame.SRCALPHA)
        self.image.blit(self.background_image, (0, 0))
        self.rect = self.image.get_rect(center=(self.player.rect.centerx, self.player.rect.centery))
        self.bound = ((WINDOW_WIDTH - WINDOW_WIDTH * 0.7) // 2, (WINDOW_HEIGHT - WINDOW_HEIGHT * 0.7) // 2)

        self.button_font = pygame.font.Font(None, 24)
        self.button_text = self.button_font.render('Close', True, (255, 255, 255))
        self.button_image = pygame.Surface((100, 50))
        self.button_image.fill((0, 0, 0))
        self.button_image.blit(self.button_text, (10, 10))
        self.button_rect = self.button_image.get_rect(
            center=(self.image.get_width() - 70, self.image.get_height() - 30))

        self.item_rect = None

    def render(self):
        self.image.blit(self.background_image, (0, 0))  # Відображаємо фон

    def update(self, dt):
        self.input()
        self.rect.center = (self.player.rect.centerx, self.player.rect.centery)
        self.render()

    def input(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0]:
            relative_mouse_pos = (mouse_pos[0] - self.bound[0] + self.button_rect.width // 2, (mouse_pos[1] - self.bound[1]))
            if self.button_rect.collidepoint(relative_mouse_pos):
                self.player.player_data.sound.mouse_click_sound.play()
                self.player.player_data.up_level()
                self.kill()
