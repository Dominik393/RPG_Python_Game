from Settings import *
from Player import Player
from NPC import NPC
from Enemy import Enemy


class MiniMap:
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
        template = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.width, self.height = template.get_size()

        background_image_width, background_image_height = self.background_image.get_size()

        for x in range(0, 7):
            for y in range(0, 6):
                template.blit(self.background_image, (x * background_image_width, y * background_image_height))

        for sprite in self.all_sprites:
            sprite_pos = (sprite.rect.x // 2, sprite.rect.y // 2)
            if isinstance(sprite, NPC):
                pygame.draw.circle(template, 'yellow', sprite_pos, self.dot_radius)
                text_surface = self.font.render(sprite.__class__.__name__, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(sprite_pos[0], sprite_pos[1] + 14))
                template.blit(text_surface, text_rect)

        return template

    def display_entities(self, crop_x, crop_y, crop_width, crop_height):
        for sprite in self.all_sprites:
            sprite_pos = ((sprite.rect.x // 2) - crop_x + WINDOW_WIDTH - crop_width - 10,
                          (sprite.rect.y // 2) - crop_y + WINDOW_HEIGHT - crop_height - 10)

            if (WINDOW_WIDTH - crop_width - 10 <= sprite_pos[0] <= WINDOW_WIDTH - 10 and
                    WINDOW_HEIGHT - crop_height - 10 <= sprite_pos[1] <= WINDOW_HEIGHT - 10):
                if isinstance(sprite, Player):
                    pygame.draw.circle(self.display_surface, 'blue', sprite_pos, self.dot_radius)
                elif isinstance(sprite, Enemy):
                    pygame.draw.circle(self.display_surface, 'red', sprite_pos, self.dot_radius)

    def draw(self, shrink_factor=0.5):
        crop_width = self.width // 2 * (1 - shrink_factor)
        crop_height = self.height // 2 * (1 - shrink_factor)

        crop_x = self.player.rect.x // 2 - crop_width // 2
        crop_y = self.player.rect.y // 2 - crop_height // 2

        crop_x = max(0, min(crop_x, self.template.get_width() - crop_width))
        crop_y = max(0, min(crop_y, self.template.get_height() - crop_height))

        crop_rect = pygame.Rect(crop_x, crop_y, crop_width, crop_height)

        subsurface = self.template.subsurface(crop_rect)

        self.display_surface.blit(subsurface,
                                  (WINDOW_WIDTH - crop_width - 10, WINDOW_HEIGHT - crop_height - 10))

        self.display_entities(crop_x, crop_y, crop_width, crop_height)

        pygame.draw.rect(self.display_surface, 'white', (WINDOW_WIDTH - crop_width - 10,
                                                         WINDOW_HEIGHT - crop_height - 10, crop_width,
                                                         crop_height), 3)
