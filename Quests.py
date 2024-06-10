from enum import Enum

from Skills import Skills
from Item import Item
from ItemType import ItemType
from Settings import *

class Quests(Enum):
    # id, name, level, prizeExp, prizeCoins, prizeHealth, prizeEquipment[], prizeSkills (?), toNextLevel (?)
    # enemiesToWin, coinsToEarn, itemsToBuy, specific_cond (?), text

    # specific_cond - for example, try Fortune, then FortuneNPC will write down that you have done this task
    FIRST_STEPS = (1, "First steps", 1, 10, 30, 0, [], False, False, 0, 10, [Item(ItemType.THREAD, 1)], False, "Buy 1 thread and earn 10 coins")
    MAGIC_DUEL = (2, "Magic duel", 1, 15, 50, 0, [Item(ItemType.ACID, 1)], False, False, 1, 0, [], True, "Try your fortune and win in one duel")
    CHAMPION = (3, "Champion", 1, 20, 60, 100, [], True, True, 2, 0, [], True, "Buy any equipment and win all magic enemies")
    THE_BEST_ASSISTANT = (4, "The best assistant", 2, 10, 25, 0, [], False, False, 0, 0, [Item(ItemType.DIAMOND, 1)], True, "Find brown buttons on the map and buy 1 diamond")
    NOT_A_NEWBIE_ANYMORE = (5, "Not a newbie anymore", 2, 30, 60, 50, [Item(ItemType.MAGIC_STONE, 1), Item(ItemType.SCISSORS, 1)], False, False, 4, 10, [], True, "Earn 10 coins and win 4 enemies")
    FASHION_ENEMIES = (6, "Fashion enemies", 2, 30, 60, 100, [[Item(ItemType.ACID, 1)]], True, True, 2, 0, [], True, "Buy any equipment and win all magic enemies")

    @property
    def id(self):
        return self.value[0]

    @property
    def name(self):
        return self.value[1]

    @property
    def level(self):
        return self.value[2]

    @property
    def prize_exp(self):
        return self.value[3]

    @property
    def prize_coins(self):
        return self.value[4]

    @property
    def prize_health(self):
        return self.value[5]

    @property
    def prize_equipment(self):
        return self.value[6]

    @property
    def prize_skills(self):
        return self.value[7]

    @property
    def to_next_level(self):
        return self.value[8]

    @property
    def enemies_to_win(self):
        return self.value[9]

    @property
    def coins_to_earn(self):
        return self.value[10]

    @property
    def items_to_buy(self):
        return self.value[11]

    @property
    def specific_cond(self):
        return self.value[12]

    @property
    def text(self):
        return self.value[13]
