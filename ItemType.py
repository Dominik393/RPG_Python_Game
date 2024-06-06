from enum import Enum
import pygame
from os.path import join
class ItemType(Enum):
    # id, price, damage, min_level_to_get, image, name
    SCISSORS = (1, 40, 1, 0, pygame.image.load(join('graphics', 'objects', 'items', 'scissors.png')), "scissors")
    HAMMER = (2, 50, 2, 5, pygame.image.load(join('graphics', 'objects', 'items', 'hammer.png')), "hammer")
    POISONOUS_SNAIL = (3, 60, 2, 10, pygame.image.load(join('graphics', 'objects', 'items', 'poisonous_snail.png')), "poisonous snail")
    MAGIC_STONE = (4, 80, 3, 15, pygame.image.load(join('graphics', 'objects', 'items', 'magic_stone.png')), "magic stone")
    SHIELD = (5, 70, 1, 20, pygame.image.load(join('graphics', 'objects', 'items', 'shield.png')), "shield")
    DIAMOND = (6, 30, 1, 0, pygame.image.load(join('graphics', 'objects', 'items', 'diamond.png')), "diamond")
    FLAMMABLE_LIQUID = (7, 10, 3, 45, pygame.image.load(join('graphics', 'objects', 'items', 'flammable_liquid.png')), "flammable liquid")
    CHEMICAL_LIQUID = (8, 120, 4, 50, pygame.image.load(join('graphics', 'objects', 'items', 'chemical_liquid.png')), "chemical liquid")
    THREAD = (9, 15, 2, 8, pygame.image.load(join('graphics', 'objects', 'items', 'thread.png')), "thread")
    ACID = (10, 75, 3, 15, pygame.image.load(join('graphics', 'objects', 'items', 'acid.png')), "acid")
    SLEEPING_FLOWER = (11, 10, 2, 0, pygame.image.load(join('graphics', 'objects', 'items', 'sleeping_flower.png')), "sleeping flower")

    @property
    def id(self):
        return self.value[0]

    @property
    def price(self):
        return self.value[1]

    @property
    def damage(self):
        return self.value[2]

    @property
    def min_level_to_get(self):
        return self.value[3]

    @property
    def image(self):
        return self.value[4]

    @property
    def name(self):
        return self.value[5]
