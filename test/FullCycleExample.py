# Setup
hero = Player("Hero", strength=8, intelligence=6, hp=100, mana=30)
enemy = AIPlayer("Goblin", strength=10, intelligence=3, hp=60, mana=10, ai_behavior=AggressiveAI())

# Actions
fireball = ManaCostAction(FireballSpell(), cost=10)
fireball = CooldownAction(fireball, cooldown_turns=2)
hero.actions.append(fireball)
hero.inventory.append(HealingPotion(20))

# Enemy actions
enemy.actions.append(CooldownAction(AttackAction(), cooldown_turns=1))

# Add status effect to enemy
enemy.status_effects.append(BurnEffect(turns=3))

# Simulate turns
for turn in range(3):
    print(f"\n--- Turn {turn + 1} ---")
    hero.start_turn()
    hero.perform_action(0, enemy)  # Try to cast fireball
    hero.tick_cooldowns()

    enemy.take_turn(hero)

    print(hero)
    print(enemy)
