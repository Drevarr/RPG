import zipfile

structure = {
    "rpg_game/": ["main.py", "__init__.py"],
    "rpg_game/core/": ["player.py", "__init__.py"],
    "rpg_game/actions/": ["base.py", "attack.py", "magic.py", "wrappers.py", "__init__.py"],
    "rpg_game/effects/": ["base.py", "conditions.py", "buffs.py", "__init__.py"],
    "rpg_game/items/": ["base.py", "potions.py", "__init__.py"],
    "rpg_game/ai/": ["behavior.py", "__init__.py"],
    "rpg_game/ui/": ["renderer.py", "__init__.py"],
    "rpg_game/utils/": ["game_loop.py", "__init__.py"]
}

file_contents = {
    "rpg_game/main.py": '''from core.player import Player, AIPlayer
from actions.attack import AttackAction
from actions.magic import FireballSpell
from actions.wrappers import ManaCostAction, CooldownAction
from effects.conditions import BurnEffect
from ai.behavior import AggressiveAI
from items.potions import HealingPotion

hero = Player("Hero", strength=8, intelligence=6, hp=100, mana=30)
enemy = AIPlayer("Goblin", strength=10, intelligence=3, hp=60, mana=10, ai_behavior=AggressiveAI())

fireball = ManaCostAction(FireballSpell(), cost=10)
fireball = CooldownAction(fireball, cooldown_turns=2)
hero.actions.append(fireball)
hero.inventory.append(HealingPotion(20))

enemy.actions.append(CooldownAction(AttackAction(), cooldown_turns=1))
enemy.status_effects.append(BurnEffect(turns=3))

for turn in range(3):
    print(f"\\n--- Turn {turn + 1} ---")
    hero.start_turn()
    hero.perform_action(0, enemy)
    hero.tick_cooldowns()
    enemy.take_turn(hero)
    print(hero)
    print(enemy)
''',

    "rpg_game/core/player.py": '''from ui.renderer import ConsoleUIRenderer

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
''',

    "rpg_game/actions/magic.py": '''from actions.base import Action

class FireballSpell(Action):
    def execute(self, user, target):
        damage = user.intelligence * 3
        user._render(f"{user.name} casts Fireball at {target.name} for {damage} fire damage!")
        target.hp -= damage
''',

    "rpg_game/actions/base.py": '''from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self, user, target):
        pass
''',

    "rpg_game/actions/wrappers.py": '''from actions.base import Action

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
''',

    "rpg_game/effects/conditions.py": '''from effects.base import StatusEffect

class BurnEffect(StatusEffect):
    def apply(self, target):
        damage = 4
        target.hp -= damage
        target._render(f"{target.name} takes {damage} burn damage!")

class StunEffect(StatusEffect):
    def apply(self, target):
        target.stunned = True
        target._render(f"{target.name} is stunned and cannot act!")
''',

    "rpg_game/effects/base.py": '''from abc import ABC, abstractmethod

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
''',

    "rpg_game/items/potions.py": '''from items.base import Item

class HealingPotion(Item):
    def __init__(self, amount):
        self.amount = amount

    def use(self, user, target):
        target.hp += self.amount
        user._render(f"{user.name} heals {target.name} for {self.amount} HP using a potion.")
''',

    "rpg_game/items/base.py": '''from abc import ABC, abstractmethod

class Item(ABC):
    @abstractmethod
    def use(self, user, target):
        pass
''',

    "rpg_game/ai/behavior.py": '''from abc import ABC, abstractmethod

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
''',

    "rpg_game/ui/renderer.py": '''class ConsoleUIRenderer:
    def display(self, message):
        print("[UI] " + message)
''',
}

# Empty __init__.py files
for folder in structure:
    for file in structure[folder]:
        if file.endswith("__init__.py") and f"{folder}{file}" not in file_contents:
            file_contents[f"{folder}{file}"] = ""

# Write to zip
with zipfile.ZipFile("rpg_game_project.zip", "w") as zipf:
    for folder, files in structure.items():
        for file in files:
            filepath = folder + file
            content = file_contents.get(filepath, f"# {file}")
            zipf.writestr(filepath, content)

print("✅ Created: rpg_game_project.zip")
