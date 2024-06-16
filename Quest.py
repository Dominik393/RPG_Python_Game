import random
from Skills import Skills
from PlayerData import PlayerData


class Quest:
    def __init__(self, player_data, quest):
        self.player_data = player_data
        self.quest = quest
        player_data.demand_coins_total += self.quest.coins_to_earn
        player_data.demand_enemies_won_total += self.quest.enemies_to_win
        self.start_player_data = PlayerData(player_data.health, player_data.coins, player_data.power,
                                            player_data.magic_power, player_data.mana, player_data.itemset)
        self.specific_cond = False
        self.prize_skill = None
        if self.quest.prize_skills: self.prize_skill = self.define_prize_skills()

    def define_prize_skills(self):
        if self.quest.prize_skills and len(self.player_data.skills) < len(list(Skills)):
            random_skill = random.choice(list(Skills))
            while random_skill in self.player_data.skills:
                random_skill = random.choice(list(Skills))
            return random_skill
        return None

    def isDone(self, player_data):
        if player_data.enemies_won_total + player_data.enemies_won_level < player_data.demand_enemies_won_total: return False
        for item in self.quest.items_to_buy:
            old_amount = self.start_player_data.inventory.find_item_amount(item)
            new_amount = player_data.inventory.find_item_amount(item)
            if old_amount + item.amount > new_amount:
                return False
        if player_data.earned_coins_total + player_data.earned_coins_level < player_data.demand_coins_total: return False

        if self.quest.specific_cond and not self.specific_cond: return False
        return True

    def rewardPlayer(self, player_data):
        player_data.exp += self.quest.prize_exp
        player_data.coins += self.quest.prize_coins
        player_data.health = min(player_data.health + self.quest.prize_health, 100)
        for item in self.quest.prize_equipment:
            player_data.inventory.add_item(item)
        player_data.skills.add(self.prize_skill)
