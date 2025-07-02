from effects.base import StatusEffect

class BurnEffect(StatusEffect):
    def apply(self, target):
        damage = 4
        target.hp -= damage
        target._render(f"{target.name} takes {damage} burn damage!")

class StunEffect(StatusEffect):
    def apply(self, target):
        target.stunned = True
        target._render(f"{target.name} is stunned and cannot act!")
