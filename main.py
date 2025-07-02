from core.player import Player, AIPlayer
from actions.attack import AttackAction
from actions.magic import FireballSpell
from actions.wrappers import ManaCostAction, CooldownAction
from effects.conditions import BurnEffect
from ai.behavior import AggressiveAI
from items.potions import HealingPotion

hero = Player("Hero", strength=8, intelligence=6, dexterity=5, wisdom = 3, hp=100, mana=30)
enemy = AIPlayer("Goblin", strength=10, intelligence=3, dexterity=4, wisdom = 2, hp=60, mana=10, ai_behavior=AggressiveAI())

fireball = ManaCostAction(FireballSpell(), cost=10)
fireball = CooldownAction(fireball, cooldown_turns=2)
hero.actions.append(fireball)
hero.inventory.append(HealingPotion(20))

enemy.actions.append(CooldownAction(AttackAction(), cooldown_turns=1))
enemy.status_effects.append(BurnEffect(turns=3))

for turn in range(3):
    print(f"\n--- Turn {turn + 1} ---")
    hero.start_turn()
    hero.perform_action(0, enemy)
    hero.tick_cooldowns()
    enemy.take_turn(hero)
    print(hero)
    print(enemy)
