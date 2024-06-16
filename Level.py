import pygame.sprite

from Enemy import Enemy
from Coin import Coin
from Fortune import Fortune
from Health import Health
from Informator import Informator
from Questgiver import Questgiver
from Settings import *
from Shopkeeper import Shopkeeper
from Sprites import Sprite
from Player import Player
from AllSprites import AllSprites
from GeneralUI import GeneralUI
from MiniMap import MiniMap
from QuestItem import QuestItem


class Level:
    def __init__(self, tmx_map, player_name, current_skin, player_data, sound):
        self.player_name = None
        self.display_surface = pygame.display.get_surface()

        self.player_name = player_name
        self.current_skin = current_skin
        self.player_data = player_data

        self.sound = sound

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.invisible_collision_sprites = pygame.sprite.Group()
        self.GUI = None

        self.player = None

        self.background_image = pygame.image.load(join('data', 'maps', 'grass.png')).convert()
        self.bg_width, self.bg_height = self.background_image.get_size()

        self.setup(tmx_map)
        self.minimap = MiniMap(self.background_image, self.all_sprites, self.player, self.display_surface)

    def setup(self, tmx_map):
        quest_dialogue = "000"
        if self.player_data.last_questgiver_dialogue is not None:
            quest_dialogue = self.player_data.last_questgiver_dialogue
        for x, y, surf in tmx_map.get_layer_by_name('BG').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
        for collision in self.collision_sprites: self.invisible_collision_sprites.add(collision)
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites,
                                     self.invisible_collision_sprites, self.player_data, self.player_name,
                                     self.current_skin, self.sound)
            elif obj.name == 'shopkeeper':
                Shopkeeper((obj.x, obj.y), self.all_sprites, self.collision_sprites, "000", self.player, 0)
            elif obj.name == 'questgiver':
                Questgiver((obj.x, obj.y), self.all_sprites, self.collision_sprites, quest_dialogue, self.player, 500)
            elif obj.name == 'informator':
                Informator((obj.x, obj.y), self.all_sprites, self.collision_sprites, "000", self.player, 1000)
            elif obj.name == 'fortune':
                Fortune((obj.x, obj.y), self.all_sprites, self.collision_sprites, "000", self.player, 1500)
            elif obj.name == 'wilddog':
                Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player, 0, 5, 45, vector(1, 0),
                      obj.name)
            elif obj.name == 'zombie':
                Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player, 0, 15, 120, vector(1, 0),
                      obj.name)
            elif obj.name == 'draft':
                Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player, 0, 8, 70, vector(1, 0),
                      obj.name)
            elif obj.name == 'ugly_angel':
                Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player, 0, 10, 80, vector(1, 0),
                      obj.name)
            elif obj.name == 'hatter':
                Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player, 0, 15, 100, vector(0, 1),
                      obj.name)
            elif obj.name == 'glasser':
                Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player, 0, 10, 95, vector(0, 1),
                      obj.name)
            elif obj.name == 'winged':
                Enemy((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player, 0, 15, 150, vector(0, 1),
                      obj.name)
            elif obj.name == 'coin':
                Coin((obj.x, obj.y), self.all_sprites, self.player)
            elif obj.name == 'health':
                Health((obj.x, obj.y), self.all_sprites, self.player)
            elif obj.name == 'brown_buttons':
                QuestItem((obj.x, obj.y), self.all_sprites, self.player, "brown_buttons")
            elif obj.name == 'blue_ball':
                QuestItem((obj.x, obj.y), self.all_sprites, self.player, "blue_ball")
            else:
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        self.GUI = GeneralUI(self.all_sprites, self.player.player_data, self.player)

    def draw_background(self):
        for x in range(0, self.display_surface.get_width(), self.bg_width):
            for y in range(0, self.display_surface.get_height(), self.bg_height):
                self.display_surface.blit(self.background_image, (x, y))

    def run(self, dt):
        self.all_sprites.update(dt)
        self.draw_background()
        self.all_sprites.draw(self.player.rect.center)
        self.GUI.update(dt)
        self.minimap.draw()
