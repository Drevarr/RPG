from items.base import Item

class HealingPotion(Item):
    def __init__(self, amount):
        self.amount = amount

    def use(self, user, target):
        target.hp += self.amount
        user._render(f"{user.name} heals {target.name} for {self.amount} HP using a potion.")
