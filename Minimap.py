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
        self.dot_radius = 8
        self.font = pygame.font.Font(None, 16)
        self.template = self.create_template()


    def create_template(self):
        # Create a new surface with the same size as the background image
        template = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.width, self.height = template.get_size()

        background_image_width, background_image_height = self.background_image.get_size()


        # Blit the background image onto the new surface
        for x in range(0, 7):
            for y in range(0, 6):
                template.blit(self.background_image, (x * background_image_width, y * background_image_height))

        # Iterate over all sprites
        for sprite in self.all_sprites:
            # If the sprite is an NPC, draw a yellow dot at its position
            sprite_pos = (sprite.rect.x // 2, sprite.rect.y // 2)
            if isinstance(sprite, NPC):
                pygame.draw.circle(template, 'yellow', sprite_pos, self.dot_radius)
                text_surface = self.font.render(sprite.__class__.__name__, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(sprite_pos[0], sprite_pos[1] + 14))
                template.blit(text_surface, text_rect)

        # Return the new surface
        return template

    def display_entities(self, crop_x, crop_y, crop_width, crop_height):
        # Create new surface that contains only the player and enemies dots
        for sprite in self.all_sprites:
            # Adjust the sprite's position based on the cropping rectangle's position
            sprite_pos = ((sprite.rect.x // 2) - crop_x + WINDOW_WIDTH - crop_width - 10,
                          (sprite.rect.y // 2) - crop_y + WINDOW_HEIGHT - crop_height - 10)

            # Check if the sprite's position is within the bounds of the minimap
            if (WINDOW_WIDTH - crop_width - 10 <= sprite_pos[0] <= WINDOW_WIDTH - 10 and
                    WINDOW_HEIGHT - crop_height - 10 <= sprite_pos[1] <= WINDOW_HEIGHT - 10):
                if isinstance(sprite, Player):
                    pygame.draw.circle(self.display_surface, 'blue', sprite_pos, self.dot_radius)
                elif isinstance(sprite, Enemy):
                    pygame.draw.circle(self.display_surface, 'red', sprite_pos, self.dot_radius)

    def draw(self, shrink_factor = 0.4):
        # Calculate the size of the cropping rectangle
        crop_width = self.width // 2 * (1 - shrink_factor)
        crop_height = self.height // 2 * (1 - shrink_factor)

        # Calculate the top-left position of the cropping rectangle
        crop_x = self.player.rect.x // 2 - crop_width // 2
        crop_y = self.player.rect.y // 2 - crop_height // 2

        # Ensure the cropping rectangle is within the bounds of the template
        crop_x = max(0, min(crop_x, self.template.get_width() - crop_width))
        crop_y = max(0, min(crop_y, self.template.get_height() - crop_height))

        # Create the cropping rectangle
        crop_rect = pygame.Rect(crop_x, crop_y, crop_width, crop_height)

        # Crop the template
        subsurface = self.template.subsurface(crop_rect)

        # Blit the cropped template onto the display surface
        self.display_surface.blit(subsurface,
                                  (WINDOW_WIDTH - crop_width - 10, WINDOW_HEIGHT - crop_height - 10))

        # Update the minimap
        self.display_entities(crop_x, crop_y, crop_width, crop_height)

        # Draw the minimap border
        pygame.draw.rect(self.display_surface, 'white', (WINDOW_WIDTH - crop_width - 10,
                                                         WINDOW_HEIGHT - crop_height - 10, crop_width,
                                                         crop_height), 3)
