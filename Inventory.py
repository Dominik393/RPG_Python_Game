class Inventory:
    def __init__(self):
        self.rows = 5
        self.columns = 4
        self.inventory = [[0 for _ in range(self.rows)] for _ in range(self.columns)]

    def add_item(self, item):
        for i in range(self.columns):
            for j in range(self.rows):
                if self.inventory[i][j] != 0 and self.inventory[i][j].item_type == item.item_type:
                    self.inventory[i][j].increase_amount(item.amount)
                    return True
                elif self.inventory[i][j] == 0:
                    self.inventory[i][j] = item
                    item.x = i
                    item.y = j
                    return True
        return False

    def remove_item(self, item):
        for i in range(self.columns):
            for j in range(self.rows):
                if self.inventory[i][j] == item:
                    result = self.inventory[i][j].decrease_amount()
                    if self.inventory[i][j].amount == 0:
                        self.inventory[i][j] = 0
                    return result
        return False

    def get_item(self, i, j):
        return self.inventory[i][j]

    def get_inventory(self):
        return self.inventory

    def get_inventory_size(self):
        return len(self.inventory)

    def item_move(self, i, j, x, y):
        self.inventory[x][y], self.inventory[i][j] = self.inventory[i][j], self.inventory[x][y]
        self.inventory[x][y].x = x
        self.inventory[x][y].y = y
        if self.inventory[i][j] != 0:
            self.inventory[i][j].x = i
            self.inventory[i][j].y = j
        return True

    def get_item_list(self):
        items = []
        for i in range(self.columns):
            for j in range(self.rows):
                if self.inventory[i][j] != 0:
                    if self.inventory[i][j].amount <= 0:
                        self.inventory[i][j] = 0
                        continue
                    items.append(self.inventory[i][j])
        return items

    def find_item_amount(self, item):
        for i in range(self.columns):
            for j in range(self.rows):
                if self.inventory[i][j] != 0 and self.inventory[i][j].item_type == item.item_type:
                    return self.inventory[i][j].amount
        return 0