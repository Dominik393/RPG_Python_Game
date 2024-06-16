import pygame
from Settings import *
from Spritessheet import SpritesSheet


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.groups = groups
        self.image = pygame.Surface((48, 56))
        self.rect = self.image.get_rect(topleft=pos)

        self.old_rect = self.rect.copy()

        my_spritesheet = SpritesSheet(f'graphics/objects/coins/texture.png')
        self.sprite_positions = [my_spritesheet.parse_sprite('1.png'), my_spritesheet.parse_sprite('2.png'),
                                 my_spritesheet.parse_sprite('3.png'), my_spritesheet.parse_sprite('4.png'),
                                 my_spritesheet.parse_sprite('5.png'), my_spritesheet.parse_sprite('6.png'),
                                 my_spritesheet.parse_sprite('7.png'), my_spritesheet.parse_sprite('8.png')]

        self.current_img = 0
        self.image = self.sprite_positions[self.current_img]
        self.player = player

        self.animation_time = 90
        self.last_update_time = pygame.time.get_ticks()

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_time:
            self.current_img = (self.current_img + 1) % len(self.sprite_positions)
            self.image = self.sprite_positions[self.current_img]
            self.last_update_time = current_time

        # Check collision with player
        if self.rect.collidepoint(self.player.rect.center):
            self.player.player_data.increase_coins(1)
            self.player.sound.coin_sound.play()
            self.player.player_data.earned_coins_level += 1
            self.kill()
