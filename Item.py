
class Item:
    def __init__(self, item_type, amount=float('inf'), usable_during_battle=True):
        self.name = item_type.name
        self.id = item_type.id
        self.image = item_type.image
        self.amount = amount
        self.usable_during_battle = usable_during_battle
        self.x = None
        self.y = None
        self.item_type = item_type
        self.price = item_type.price
        self.description = f"Price: {self.price}, Damage: {item_type.damage}, Min Level: {item_type.min_level_to_get}"

    def decrease_amount(self):
        if self.amount > 0:
            self.amount -= 1
            return True
        return False

    def use(self, player, enemy):
        if self.decrease_amount():
            enemy.enemy_data.reduce_health(self.item_type.value[2])
            return True
        return False

    def increase_amount(self, amount=1):
        self.amount += amount
        return True

    def __str__(self):
        return self.name
