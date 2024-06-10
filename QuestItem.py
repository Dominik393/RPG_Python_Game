import pygame

import Quests
from Settings import *
from Spritessheet import SpritesSheet


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, name):
        super().__init__(groups)
        self.groups = groups
        self.image = pygame.Surface((48, 56))
        self.rect = self.image.get_rect(topleft=pos)

        self.image = self.sprite_positions[self.current_img]
        self.player = player

        self.name = name

    def update(self, dt):
        if self.rect.collidepoint(self.player.rect.center):
            if self.name == "brown_buttons" and self.player.player_data.quest is not None and self.player.player_data.quest.quest == Quests.THE_BEST_ASSISTANT:
                self.player.player_data.quest.specific_cond = True
                self.kill()
