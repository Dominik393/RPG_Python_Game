from Settings import *


class Health(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.groups = groups
        self.image = pygame.Surface((64, 57))
        self.rect = self.image.get_rect(topleft=pos)

        self.image = pygame.image.load(join('graphics', 'objects', 'health.png'))
        self.player = player

    def update(self, dt):
        if self.rect.collidepoint(self.player.rect.center):
            self.player.player_data.increase_health(self.player.player_data.level * 5)
            self.player.sound.health_sound.play()
            self.kill()
