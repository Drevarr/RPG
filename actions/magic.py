from actions.base import Action

class FireballSpell(Action):
    def execute(self, user, target):
        damage = user.intelligence * 3
        user._render(f"{user.name} casts Fireball at {target.name} for {damage} fire damage!")
        target.hp -= damage
