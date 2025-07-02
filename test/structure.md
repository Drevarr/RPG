rpg_game/
│
├── __init__.py
├── main.py                  # Entry point
│
├── core/
│   ├── __init__.py
│   ├── player.py            # Player, AIPlayer
│   ├── stats.py             # Stats or attributes (optional)
│
├── actions/
│   ├── __init__.py
│   ├── base.py              # Action ABC
│   ├── attack.py            # AttackAction
│   ├── magic.py             # FireballSpell, etc.
│   ├── wrappers.py          # ManaCostAction, CooldownAction
│
├── effects/
│   ├── __init__.py
│   ├── base.py              # StatusEffect, Effect ABC
│   ├── conditions.py        # StunEffect, BurnEffect
│   ├── buffs.py             # DefenseBuff, etc.
│
├── items/
│   ├── __init__.py
│   ├── base.py              # Item ABC
│   ├── potions.py           # HealingPotion, ManaPotion
│
├── ai/
│   ├── __init__.py
│   ├── behavior.py          # AIBehavior, AggressiveAI
│
├── ui/
│   ├── __init__.py
│   ├── renderer.py          # ConsoleUIRenderer, GUIRenderer
│
└── utils/
    ├── __init__.py
    ├── game_loop.py         # Optional: Game loop / battle manager
