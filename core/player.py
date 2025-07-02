from ui.renderer import ConsoleUIRenderer

class Player:
    def __init__(self, name, strength, intelligence, hp, mana):
        self.name = name
        self.strength = strength
        self.intelligence = intelligence
        self.hp = hp
        self.mana = mana
        self.defense = 0
        self.actions = []
        self.effects = []
        self.status_effects = []
        self.inventory = []
        self.stunned = False
        self.ui_renderer = ConsoleUIRenderer()

    def perform_action(self, index, target):
        if self.stunned:
            self._render(f"{self.name} is stunned and skips the turn!")
            return
        if 0 <= index < len(self.actions):
            self.actions[index].execute(self, target)
        else:
            self._render("Invalid action index!")

    def use_item(self, index, target):
        if 0 <= index < len(self.inventory):
            item = self.inventory.pop(index)
            item.use(self, target)
        else:
            self._render("Invalid item index!")

    def start_turn(self):
        self.stunned = False
        for effect in self.status_effects:
            effect.apply(self)
            effect.tick()
        self.status_effects = [e for e in self.status_effects if not e.is_expired()]

    def tick_cooldowns(self):
        for action in self.actions:
            if hasattr(action, "tick"):
                action.tick()

    def _render(self, message):
        if self.ui_renderer:
            self.ui_renderer.display(message)
        else:
            print(message)

    def __str__(self):
        return f"{self.name} [HP: {self.hp}, Mana: {self.mana}, DEF: {self.defense}]"

class AIPlayer(Player):
    def __init__(self, name, strength, intelligence, hp, mana, ai_behavior):
        super().__init__(name, strength, intelligence, hp, mana)
        self.ai_behavior = ai_behavior

    def take_turn(self, opponent):
        self.start_turn()
        if self.stunned:
            return
        action_index = self.ai_behavior.choose_action(self, opponent)
        if action_index is not None:
            self.perform_action(action_index, opponent)
        self.tick_cooldowns()
