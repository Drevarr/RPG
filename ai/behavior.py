from abc import ABC, abstractmethod

class AIBehavior(ABC):
    @abstractmethod
    def choose_action(self, user, target):
        pass

class AggressiveAI(AIBehavior):
    def choose_action(self, user, target):
        for i, action in enumerate(user.actions):
            if hasattr(action, "remaining_cooldown") and action.remaining_cooldown > 0:
                continue
            return i
        return None
