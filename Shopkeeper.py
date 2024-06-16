from Quests import Quests
from Inventory import Inventory
from Item import Item
from ItemType import ItemType
from NPC import NPC
from ShopInventoryUI import ShopInventoryUI


def can_sell_equipment(equipment, player):
    return player.player_data.coins >= equipment.price


def sell_equipment(equipment, player):
    if can_sell_equipment(equipment, player):
        player.player_data.coins -= equipment.price
        player.sound.money_sound.play()
        player.player_data.inventory.add_item(Item(equipment.item_type, 1))
        if player.player_data.quest is not None and \
                (player.player_data.quest.quest == Quests.CHAMPION
                 or player.player_data.quest.quest == Quests.FASHION_ENEMIES
                 or player.player_data.quest.quest == Quests.STRONG_MAGICIAN):
            player.player_data.quest.specific_cond = True
        return True
    return False


class Shopkeeper(NPC):
    def __init__(self, pos, groups, collision_sprites, current_dialogue, player, timer):
        super().__init__(pos, groups, collision_sprites, current_dialogue, player, timer)
        self.inventory = Inventory()
        self.populate_inventory()
        self.inventoryUI = None

    def populate_inventory(self):
        for item_type in ItemType:
            if self.player.player_data.level >= item_type.min_level_to_get:
                self.inventory.add_item(Item(item_type))

    def dialogue(self):
        responses, last_dialogue = super().dialogue()
        if len(responses) > 0 and responses[0] == 0:
            self.inventoryUI = ShopInventoryUI(self.groups, self.inventory, self.player, self)