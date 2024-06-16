class EntityData:
    def __init__(self, health, max_health, power, magic_power=0, skills=None):
        if health < 0:
            raise ValueError("Health cannot be negative")
        if power < 0:
            raise ValueError("Power cannot be negative")
        if max_health < 0:
            raise ValueError("Max health cannot be negative")

        self.power = power
        self.magic_power = magic_power
        self.max_health = max_health
        if health > max_health:
            self.health = max_health
        else:
            self.health = health
        if skills is None:
            self.skills = []
        else:
            self.skills = skills

        self.damage = 0

    def reduce_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def increase_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
