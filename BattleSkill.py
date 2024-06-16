import math
from Notification import *

class BattleSkill:
    def __init__(self, power, mana_cost, name):
        self.power = power
        self.mana_cost = mana_cost
        self.name = name

    def validation(self, player):
        if player.player_data.mana < self.mana_cost:
            return False, Notification("Not enough mana", 100)
        return True, None

    def use(self, player, _enemy):
        if not self.validation(player)[0]:
            return False
        player.player_data.mana -= self.mana_cost
        return True

    def effect(self, player, enemy):
        raise NotImplementedError("Skill not implemented yet")

    def __str__(self):
        return self.name


class Heal(BattleSkill):
    def __init__(self):
        super().__init__(2, 3, "Heal")

    def effect(self, player, _enemy):
        if not super().use(player, _enemy):
            return False

        player.player_data.increase_health(self.power + math.ceil(player.player_data.magic_power * 0.1))

class Fireball(BattleSkill):
    def __init__(self):
        super().__init__(2, 4, "Fireball")

    def effect(self, player, enemy):
        if not super().use(player, enemy):
            return False

        enemy.enemy_data.reduce_health(self.power + math.ceil(player.player_data.magic_power * 0.2))
        if enemy.enemy_data.health <= 0:
            return True
        return False

class Protect(BattleSkill):
    def __init__(self):
        super().__init__(0, 2, "Protect")


    def effect(self, player, _enemy):
        if not super().use(player, _enemy):
            return False

        player.status_effects.protected = True
