from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self, user, target):
        pass
