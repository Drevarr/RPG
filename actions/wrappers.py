from actions.base import Action

class ManaCostAction(Action):
    def __init__(self, action, cost):
        self.action = action
        self.cost = cost

    def execute(self, user, target):
        if user.mana >= self.cost:
            user.mana -= self.cost
            user._render(f"{user.name} uses {self.cost} mana.")
            self.action.execute(user, target)
        else:
            user._render(f"{user.name} doesn't have enough mana!")

class CooldownAction(Action):
    def __init__(self, action, cooldown_turns):
        self.action = action
        self.cooldown_turns = cooldown_turns
        self.remaining_cooldown = 0

    def execute(self, user, target):
        if self.remaining_cooldown == 0:
            self.action.execute(user, target)
            self.remaining_cooldown = self.cooldown_turns
            user._render(f"{self.action.__class__.__name__} is on cooldown.")
        else:
            user._render(f"{self.action.__class__.__name__} is cooling down ({self.remaining_cooldown} turns).")

    def tick(self):
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= 1
