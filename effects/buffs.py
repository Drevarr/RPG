from effects.base import StatusEffect

class MagicArmor(StatusEffect):
    def __init__(self, turns, bonus_armor):
        super().__init__(turns)
        self.bonus_armor = bonus_armor
        self.applied = False

    def apply(self, target):
        if not self.applied:
            target.armor += self.bonus_armor
            self.applied = True
        if self.is_expired():
            target.armor -= self.bonus_armor

    def can_stack_with(self, other):
        return isinstance(other, MagicArmor) and other.bonus_armor >= self.bonus_armor

    def stack_with(self, other):
        # Extend duration only if new effect is equal or stronger
        self.remaining_turns = max(self.remaining_turns, other.remaining_turns)


class Invisibility(StatusEffect):
    def __init__(self, turns):
        super().__init__(turns)
        self.applied = False

    def apply(self, target):
        if not self.applied:
            target.invisible = True
            self.applied = True
        if self.is_expired():
            target.invisible = False
