from Quests import Quests
from Settings import *


class QuestItem(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, name):
        super().__init__(groups)
        self.groups = groups
        self.image = pygame.Surface((64, 57))
        self.rect = self.image.get_rect(topleft=pos)

        self.name = name

        self.image = pygame.image.load(join('graphics', 'objects', 'items', f'{name}.png'))
        self.player = player

    def update(self, dt):
        if self.rect.collidepoint(self.player.rect.center):
            if self.name == "brown_buttons" and self.player.player_data.quest is not None and self.player.player_data.quest.quest == Quests.THE_BEST_ASSISTANT:
                self.player.player_data.quest.specific_cond = True
                self.player.sound.quest_item_sound.play()
                self.kill()
            elif self.name == "blue_ball" and self.player.player_data.quest is not None and self.player.player_data.quest.quest == Quests.STRONG_MAGICIAN:
                self.player.player_data.quest.specific_cond = True
                self.player.sound.quest_item_sound.play()
                self.kill()
