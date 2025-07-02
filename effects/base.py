from abc import ABC, abstractmethod

class StatusEffect(ABC):
    def __init__(self, turns):
        self.remaining_turns = turns

    @abstractmethod
    def apply(self, target):
        pass

    def tick(self):
        self.remaining_turns -= 1

    def is_expired(self):
        return self.remaining_turns <= 0
