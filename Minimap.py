import pygame

from Settings import *
from Player import Player
from NPC import NPC
from Enemy import Enemy
from Sprites import Sprite


class Minimap:
    def __init__(self, background_image, all_sprites, player, display_surface):
        self.background_image = background_image
        self.all_sprites = all_sprites
        self.player = player
        self.display_surface = display_surface
        self.width = None
        self.height = None
        self.template = self.create_template()


    def create_template(self):
        # Create a new surface with the same size as the background image
        template = pygame.Surface((WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.width, self.height = template.get_size()

        background_image_width, background_image_height = self.background_image.get_size()


        # Blit the background image onto the new surface
        for x in range(0, 5):
            for y in range(0, 5):
                template.blit(self.background_image, (x * background_image_width, y * background_image_height))

        # Iterate over all sprites
        for sprite in self.all_sprites:
            # If the sprite is an NPC, draw a yellow dot at its position
            sprite_pos = (sprite.rect.x // 2, sprite.rect.y // 2)
            if isinstance(sprite, NPC):
                pygame.draw.circle(template, 'yellow', sprite_pos, 11)

        # Return the new surface
        return template


    def update(self):
        # Create new surface that contains only the player and enemies dots

        for sprite in self.all_sprites:
            sprite_pos = (sprite.rect.x // 2 + WINDOW_WIDTH - self.width - 10, sprite.rect.y // 2 + WINDOW_HEIGHT - self.height - 1)
            if isinstance(sprite, Player):
                pygame.draw.circle(self.display_surface, 'blue', sprite_pos, 11)
            elif isinstance(sprite, Enemy):
                pygame.draw.circle(self.display_surface, 'red', sprite_pos, 11)


    def draw(self):
        self.display_surface.blit(self.template, (WINDOW_WIDTH - self.width - 10, WINDOW_HEIGHT - self.height - 10))
        self.update()
