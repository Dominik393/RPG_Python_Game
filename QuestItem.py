import pygame

from Quests import Quests
from Settings import *
from Spritessheet import SpritesSheet


class QuestItem(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, name):
        super().__init__(groups)
        self.groups = groups
        self.image = pygame.Surface((64, 57))
        self.rect = self.image.get_rect(topleft=pos)

        self.image = pygame.image.load(join('graphics', 'objects', 'items', 'brown_buttons.png'))
        self.player = player

        self.name = name

    def update(self, dt):
        if self.rect.collidepoint(self.player.rect.center):
            if self.name == "brown_buttons" and self.player.player_data.quest is not None and self.player.player_data.quest.quest == Quests.THE_BEST_ASSISTANT:
                self.player.player_data.quest.specific_cond = True
                self.kill()
