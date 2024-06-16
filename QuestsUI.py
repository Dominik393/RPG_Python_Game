import pygame
from os.path import join
from Settings import WINDOW_WIDTH, WINDOW_HEIGHT
from WindowUI import WindowUI


class QuestsUI(WindowUI):
    def __init__(self, groups, player):
        super().__init__(groups, player)

        self.coin_icon = pygame.image.load(join('graphics', 'objects', 'coin.png')).convert_alpha()
        self.health_icon = pygame.image.load(join('graphics', 'objects', 'health.png')).convert_alpha()
        self.exp_icon = pygame.image.load(join('graphics', 'objects', 'exp.png')).convert_alpha()

        self.image.fill('white')
        self.rect = self.image.get_rect(center=(self.player.rect.centerx, self.player.rect.centery))
        self.bound = ((WINDOW_WIDTH - WINDOW_WIDTH * 0.7) // 2, (WINDOW_HEIGHT - WINDOW_HEIGHT * 0.7) // 2)

        self.paragraph = self.image.get_height() // 2 - 20
        self.equipment_paragraph = 0
        self.skills_paragraph = 0

        if self.player.player_data.quest is None:
            self.message = "You haven`t any quests now. You can ask Questgiver about them!"
            self.ui_image = pygame.image.load(join('graphics', 'objects', 'ask.png'))
        elif self.player.player_data.quest.isDone(self.player.player_data):
            self.message = "You have completed all quest tasks. Meet the Questgiver to get prize!"
            self.ui_image = pygame.image.load(join('graphics', 'objects', 'done.png'))
        else:
            self.message = "Your quest: " + self.player.player_data.quest.quest.name
            self.additional_message = self.player.player_data.quest.quest.text
            self.ui_image = None
            self.prizeExp = self.player.player_data.quest.quest.prize_exp
            self.prizeCoins = self.player.player_data.quest.quest.prize_coins
            self.prizeHealth = self.player.player_data.quest.quest.prize_health
            self.prizeEquipment = self.player.player_data.quest.quest.prize_equipment
            self.prizeSkill = self.player.player_data.quest.prize_skill
            self.paragraph = 60

            if len(self.prizeEquipment) > 0: self.equipment_paragraph = 60
            if self.prizeSkill is not None: self.skills_paragraph = 60

        self.item_rect = None

    def render(self):
        self.image.fill('white')

        if self.ui_image:
            self.item_rect = self.ui_image.get_rect(
                center=(self.image.get_width() // 2, self.image.get_height() - self.image.get_height() // 3 - 30))
            self.image.blit(self.ui_image, self.item_rect)

        text_surface = self.font.render(self.message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, self.paragraph))
        self.image.blit(text_surface, text_rect)

        if hasattr(self, 'additional_message'):
            additional_text_surface = self.font.render(self.additional_message, True, (0, 0, 0))
            additional_text_rect = additional_text_surface.get_rect(
                center=(self.image.get_width() // 2, self.image.get_height() // 2 - 160))
            self.image.blit(additional_text_surface, additional_text_rect)

        if hasattr(self, 'additional_message'):
            explicite_text_surface = self.font.render("Awards:", True, (0, 0, 0))
            explicite_text_rect = explicite_text_surface.get_rect(center=(self.image.get_width() // 2,
                                                                          self.image.get_height() // 2 + 5 - self.equipment_paragraph - self.skills_paragraph))
            self.image.blit(explicite_text_surface, explicite_text_rect)

        if hasattr(self, 'prizeExp'):
            exp_text_surface = self.font.render(f"Exp: {self.prizeExp}", True, (0, 0, 0))
            exp_text_rect = exp_text_surface.get_rect(
                center=(self.image.get_width() // 2 - 150,
                        self.image.get_height() // 2 + 40 - self.equipment_paragraph - self.skills_paragraph))
            exp_icon_rect = self.exp_icon.get_rect(center=(exp_text_rect.centerx, exp_text_rect.centery + 40))
            self.image.blit(self.exp_icon, exp_icon_rect)
            self.image.blit(exp_text_surface, exp_text_rect)

        if hasattr(self, 'prizeCoins'):
            coins_text_surface = self.font.render(f"Coins: {self.prizeCoins}", True, (0, 0, 0))
            coins_text_rect = coins_text_surface.get_rect(
                center=(self.image.get_width() // 2,
                        self.image.get_height() // 2 + 40 - self.equipment_paragraph - self.skills_paragraph))
            coins_icon_rect = self.coin_icon.get_rect(center=(coins_text_rect.centerx, coins_text_rect.centery + 40))
            self.image.blit(self.coin_icon, coins_icon_rect)
            self.image.blit(coins_text_surface, coins_text_rect)

        if hasattr(self, 'prizeHealth'):
            health_text_surface = self.font.render(f"Health: {self.prizeHealth}", True, (0, 0, 0))
            health_text_rect = health_text_surface.get_rect(
                center=(self.image.get_width() // 2 + 150,
                        self.image.get_height() // 2 + 40 - self.equipment_paragraph - self.skills_paragraph))
            health_icon_rect = self.health_icon.get_rect(
                center=(health_text_rect.centerx, health_text_rect.centery + 40))
            self.image.blit(self.health_icon, health_icon_rect)
            self.image.blit(health_text_surface, health_text_rect)

        if hasattr(self, 'prizeEquipment') and len(self.prizeEquipment) > 0:
            equipment_text_surface = self.font.render("Equipment:", True, (0, 0, 0))
            equipment_text_rect = equipment_text_surface.get_rect(
                center=(self.image.get_width() // 2,
                        self.image.get_height() // 2 + 20 + abs(self.equipment_paragraph - self.skills_paragraph)))
            self.image.blit(equipment_text_surface, equipment_text_rect)
            equipment_amount = len(self.prizeEquipment)
            step = 20
            image_width = 64
            width = image_width * equipment_amount + step * (equipment_amount - 2)
            start = equipment_text_rect.centerx - width // 2 + step
            for item in self.prizeEquipment:
                item_image = pygame.image.load(item.item_type.image)
                item_rect = item_image.get_rect(center=(start, equipment_text_rect.centery + 50))
                self.image.blit(item_image, item_rect)
                start += (image_width + step)

        if hasattr(self, 'prizeSkill') and self.prizeSkill:
            skills_text_surface = self.font.render("Skills:", True, (0, 0, 0))
            skills_text_rect = skills_text_surface.get_rect(
                center=(self.image.get_width() // 2, self.image.get_height() // 2 + 70 + self.equipment_paragraph))
            self.image.blit(skills_text_surface, skills_text_rect)
            step = 20
            image_width = 64
            width = image_width - step
            start = skills_text_rect.centerx - width // 2 + step

            skill_image = self.prizeSkill.image
            skill_rect = skill_image.get_rect(center=(start, skills_text_rect.centery + 40))
            self.image.blit(skill_image, skill_rect)
            start += (image_width + step)

        self.image.blit(self.button_image, self.button_rect)
