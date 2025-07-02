# attack.py
from actions.base import Action

class AttackAction(Action):
    def execute(self, user, target):
        # Calculate damage based on user strength and target defense
        base_damage = user.strength
        if hasattr(target, 'defense'):  # If the target has defense attribute
            damage = max(base_damage - target.defense, 0)  # No negative damage
        else:
            damage = base_damage

        # Perform attack and show the result
        user._render(f"{user.name} attacks {target.name} for {damage} physical damage!")
        target.hp -= damage

        # Optionally, handle effects like "stun" or "knockback" here
        if target.hp <= 0:
            target._render(f"{target.name} has been defeated!")
