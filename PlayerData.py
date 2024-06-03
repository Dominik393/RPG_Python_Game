import random


from Skills import Skills
from ItemType import ItemType
from Settings import *
from Item import Item
from Inventory import Inventory


available_items = {
    0: [ItemType.SCISSORS, ItemType.HAMMER, ItemType.POISONOUS_SNAIL],
    1: [ItemType.MAGIC_STONE, ItemType.SHIELD, ItemType.DIAMOND],
    2: [ItemType.FLAMMABLE_LIQUID, ItemType.CHEMICAL_LIQUID, ItemType.THREAD],
    3: [ItemType.ACID, ItemType.SLEEPING_FLOWER, ItemType.THREAD],
    4: [ItemType.SCISSORS, ItemType.HAMMER, ItemType.POISONOUS_SNAIL],
    5: [ItemType.MAGIC_STONE, ItemType.SHIELD, ItemType.DIAMOND],
    6: [ItemType.FLAMMABLE_LIQUID, ItemType.CHEMICAL_LIQUID, ItemType.THREAD],
    7: [ItemType.ACID, ItemType.SLEEPING_FLOWER, ItemType.THREAD]
}


class PlayerData:

    def __init__(self, health=100, coins=30, power=1, itemset=None, timer=0):
        self.health = health
        self.coins = coins
        self.power = power
        self.skills = set()
        self.inventory = Inventory()
        self.timer = timer
        self.quest = None
        self.exp = 0
        self.itemset = itemset
        self.level = 1

        # Player can earn coins only by collecting coins on map, speaking with Fortune and winning enemies
        # In these variables we don`t add earned coins in quests
        self.earned_coins_total = 0
        self.earned_coins_level = 0
        self.demand_coins_total = 0

        self.enemies_won_total = 0
        self.enemies_won_level = 0
        self.demand_enemies_won_total = 0

        if self.itemset is None:
            self.itemset = random.choice(list(available_items.keys())) + 1
        else:
            print((self.itemset - 1) % len(Skills))
        for item in available_items[self.itemset - 1]: self.inventory.add_item(Item(item, 3))

        self.skills.add(list(Skills)[(self.itemset - 1) % len(Skills)])

    def up_level(self):
        self.earned_coins_total += self.earned_coins_level
        self.enemies_won_total += self.enemies_won_level

        self.level += 1
        self.earned_coins_level = 0
        self.enemies_won_level = 0