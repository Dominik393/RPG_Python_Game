import pygame.freetype
import pygame.image
from os.path import join
from QuestsUI import QuestsUI
from Settings import *
from InventoryUI import InventoryUI


class GeneralUI:
    def __init__(self, groups, player_data, player):
        self.display_surface = pygame.display.get_surface()
        self.player_data = player_data
        self.player = player
        self.groups = groups

        self.inventory = None
        self.quests = None
        self.last_input = pygame.time.get_ticks()

        self.font = pygame.freetype.Font(None, 30)

        self.coin_icon = pygame.image.load(join('graphics', 'objects', 'coin.png')).convert_alpha()
        self.power_icon = pygame.image.load(
            join('graphics', 'objects', 'power.png')).convert_alpha()  # Приклад шляху до іконки сили
        self.health_icon = pygame.image.load(
            join('graphics', 'objects', 'health.png')).convert_alpha()  # Приклад шляху до іконки здоров'я
        self.timer_icon = pygame.image.load(
            join('graphics', 'objects', 'timer.png')).convert_alpha()  # Завантаження іконки таймера
        self.quests_icon = pygame.image.load(
            join('graphics', 'objects', 'quests.png')).convert_alpha()  # Завантаження іконки tasks
        self.exp_icon = pygame.image.load(
            join('graphics', 'objects', 'exp.png')).convert_alpha()  # Завантаження іконки exp

    def create_inventory(self):
        self.inventory = InventoryUI(self.groups, self.player.player_data.inventory, self.player)

    def create_quests(self):
        self.quests = QuestsUI(self.groups, self.player)

    def input(self):
        keys = pygame.key.get_pressed()
        if pygame.time.get_ticks() - self.last_input < 190:
            return
        if keys[pygame.K_i] and self.inventory is None:
            self.create_inventory()
        elif keys[pygame.K_i] and self.inventory is not None:
            self.inventory.kill()
            self.inventory = None

        self.last_input = pygame.time.get_ticks()

    def check_tasks_button_click(self, mouse_pos):
        tasks_button_rect = self.quests_icon.get_rect(topleft=(30, 90))
        if tasks_button_rect.collidepoint(mouse_pos):
            if self.quests is None:
                self.player.player_data.sound.mouse_click_sound.play()
                self.create_quests()
            else:
                self.quests.kill()
                self.quests = None

    def update(self, dt):
        self.input()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.check_tasks_button_click(event.pos)

        if self.inventory is not None:
            self.inventory.update(dt)

        self.render_coins()
        self.render_power()
        self.render_health()
        self.render_exp()
        self.render_timer()
        self.render_tasks_button()
        self.render_level()

    def render_coins(self):

        coin_text = str(self.player_data.coins)
        coin_surface, coin_rect = self.font.render(coin_text, 'white')

        coin_icon_rect = self.coin_icon.get_rect(topleft=(WINDOW_WIDTH - 230, 30))

        coin_rect.midleft = (coin_icon_rect.right + 5, coin_icon_rect.centery)

        self.display_surface.blit(self.coin_icon, coin_icon_rect)
        self.display_surface.blit(coin_surface, coin_rect)

    def render_power(self):

        power_text = str(self.player_data.power)
        power_surface, power_rect = self.font.render(power_text, 'white')

        power_icon_rect = self.power_icon.get_rect(topleft=(WINDOW_WIDTH - 120, 30))

        power_rect.midleft = (power_icon_rect.right + 5, power_icon_rect.centery)

        self.display_surface.blit(self.power_icon, power_icon_rect)
        self.display_surface.blit(power_surface, power_rect)

    def render_health(self):
        health_text = str(self.player_data.health)
        health_surface, health_rect = self.font.render(health_text, 'white')

        health_icon_rect = self.health_icon.get_rect(topleft=(30, 30))

        health_rect.midleft = (health_icon_rect.right + 5, health_icon_rect.centery)

        self.display_surface.blit(self.health_icon, health_icon_rect)
        self.display_surface.blit(health_surface, health_rect)

    def render_timer(self):
        if self.player_data.timer != 0:
            timer_seconds = self.player_data.timer // 1000
            timer_text = str(timer_seconds)
            timer_surface, timer_rect = self.font.render(timer_text, 'white')

            timer_icon_rect = self.timer_icon.get_rect(center=(WINDOW_WIDTH // 2 - 18, 100))

            timer_rect.midleft = (timer_icon_rect.right + 5, timer_icon_rect.centery)

            self.display_surface.blit(self.timer_icon, timer_icon_rect)
            self.display_surface.blit(timer_surface, timer_rect)

    def render_exp(self):
        exp_text = str(self.player_data.exp)
        exp_surface, exp_rect = self.font.render(exp_text, 'white')

        exp_icon_rect = self.exp_icon.get_rect(topleft=(150, 30))

        exp_rect.midleft = (exp_icon_rect.right + 5, exp_icon_rect.centery)

        self.display_surface.blit(self.exp_icon, exp_icon_rect)
        self.display_surface.blit(exp_surface, exp_rect)

    def render_tasks_button(self):
        quests_icon_rect = self.quests_icon.get_rect(topleft=(30, 90))

        self.display_surface.blit(self.quests_icon, quests_icon_rect)

    def render_level(self):
        level_text = f'Level: {self.player.player_data.level}'
        level_surface, level_rect = self.font.render(level_text, 'white')

        level_rect.center = (WINDOW_WIDTH // 2, 50)

        self.display_surface.blit(level_surface, level_rect)
