import pygame
from os.path import join
from Settings import WINDOW_WIDTH, WINDOW_HEIGHT


class FortuneUI(pygame.sprite.Sprite):
    def __init__(self, groups, player, fortune, message, item_icon=None):
        super().__init__(groups)
        self.player = player
        self.fortune = fortune
        self.font = pygame.font.Font(None, 36)
        self.message = message  # Зберігаємо текст повідомлення
        self.item_icon = item_icon  # Зберігаємо зображення предмета

        # Збільшуємо ширину вікна та розміщуємо по центру екрану відносно гравця
        self.image = pygame.Surface((WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.7))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=(self.player.rect.centerx, self.player.rect.centery))
        self.bound = ((WINDOW_WIDTH - WINDOW_WIDTH * 0.7) // 2, (WINDOW_HEIGHT - WINDOW_HEIGHT * 0.7) // 2)

        # Створюємо кнопку
        self.button_font = pygame.font.Font(None, 24)
        self.button_text = self.button_font.render('Close', True, (255, 255, 255))
        self.button_image = pygame.Surface((100, 50))
        self.button_image.fill((0, 0, 0))
        self.button_image.blit(self.button_text, (10, 10))
        self.button_rect = self.button_image.get_rect(
            center=(self.image.get_width() - 70, self.image.get_height() - 30))

        self.item_rect = None

    def render(self):
        self.image.fill('white')

        # Якщо передано зображення предмета, відобразимо його
        if self.item_icon:
            self.item_rect = self.item_icon.get_rect(
                center=(self.image.get_width() // 2, self.image.get_height() - self.image.get_height() // 3))
            self.image.blit(self.item_icon, self.item_rect)

        # Відображення повідомлення
        text_surface = self.font.render(self.message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
        self.image.blit(text_surface, text_rect)

        # Відображення кнопки
        self.image.blit(self.button_image, self.button_rect)

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
                self.kill()
