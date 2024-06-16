from enum import Enum
from os.path import join


class ItemType(Enum):
    # id, price, damage, min_level_to_get, image, name
    THREAD = (1, 15, 20, 1, join('graphics', 'objects', 'items', 'thread.png'), "thread")
    SCISSORS = (2, 10, 10, 1, join('graphics', 'objects', 'items', 'scissors.png'), "scissors")
    HAMMER = (3, 30, 40, 1, join('graphics', 'objects', 'items', 'hammer.png'), "hammer")
    POISONOUS_SNAIL = (4, 50, 50, 1, join('graphics', 'objects', 'items', 'poisonous_snail.png'), "poisonous snail")
    MAGIC_STONE = (5, 40, 50, 1, join('graphics', 'objects', 'items', 'magic_stone.png'), "magic stone")
    SHIELD = (6, 60, 10, 2, join('graphics', 'objects', 'items', 'shield.png'), "shield")
    DIAMOND = (7, 30, 35, 2, join('graphics', 'objects', 'items', 'diamond.png'), "diamond")
    ACID = (8, 15, 30, 2, join('graphics', 'objects', 'items', 'acid.png'), "acid")
    FLAMMABLE_LIQUID = (9, 100, 70, 3, join('graphics', 'objects', 'items', 'flammable_liquid.png'), "flammable liquid")
    CHEMICAL_LIQUID = (10, 120, 65, 3, join('graphics', 'objects', 'items', 'chemical_liquid.png'), "chemical liquid")
    SLEEPING_FLOWER = (11, 140, 80, 3, join('graphics', 'objects', 'items', 'sleeping_flower.png'), "sleeping flower")

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
