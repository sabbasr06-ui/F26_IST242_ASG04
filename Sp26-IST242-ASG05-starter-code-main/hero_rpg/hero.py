"""
hero.py
=======
Hero class for the Hero Quest RPG.

Collections used (and why):
  list  (inside Bag) — ordered inventory slots
  set                — unique skills; O(1) membership test
  dict               — named stats with O(1) key lookup
  Counter            — automatic kill counting; .most_common() support
  defaultdict(list)  — group items by type without KeyError on first key
  deque(maxlen=10)   — fixed-size rolling combat log; O(1) both ends

Imports from:
  enums.py  — ItemType
  models.py — Weapon, Item
  bag.py    — Bag[T]
"""

from collections import defaultdict, Counter, deque
# from hero_rpg.enums   import ItemType
# from hero_rpg.models  import Weapon, Item
# from hero_rpg.bag     import Bag
from hero_rpg import ItemType, Weapon, Item, Bag


class Hero:
    """
    The main player character, modeling all RPG attributes
    via appropriate Python collection types.
    """

    def __init__(self, name: str, hero_class: str, max_health: int = 100) -> None:
        self.name = name
        self.hero_class = hero_class

        self.max_health = max_health
        self.health = max_health

        self.equipped_weapons: Bag[Weapon] = Bag(3)
        self.weapons = self.equipped_weapons
        self.skills: set[str] = set()
        self.inventory: Bag[Item] = Bag(20)

        self.stats: dict[str, int] = {
            "strength": 10,
            "defense": 5,
            "dexterity": 10,
            "intelligence": 10,
        }
        self.kill_counts: Counter[str] = Counter()
        self.kill_counter: Counter[str] = self.kill_counts
        self._item_registry: defaultdict[str, list[Item]] = defaultdict(list)
        self.combat_log: deque[str] = deque(maxlen=10)

        def __str__(self) -> str:
         return (
            f"Hero: {self.name} |"
            f" Class: {self.hero_class} |"
            f" Health: {self.health}/{self.max_health}"
        )

    # ── Health ────────────────────────────────────────────────────────────────

    def take_damage(self, amount: int) -> int:
        """
        Apply incoming damage, clamped so HP never drops below 0.

        Returns:
            Actual HP lost (may be less than `amount` near death).
        """
        old_health = self.health
        self.health = max(0, self.health - amount)
        actual_damage = old_health - self.health
        self.combat_log.append(
            f"{self.name} took {actual_damage} damage"
        )
        return actual_damage

    def heal(self, amount: int) -> int:
        """
        Restore HP, capped at max_health.

        Returns:
            Actual HP restored (may be less if already near full).
        """
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        actual_healing = self.health - old_health
        self.combat_log.append(
            f"{self.name} healed {actual_healing} HP"
        )
        return actual_healing

    def is_alive(self) -> bool:
        """Return True as long as health is above zero."""
        return self.health > 0

    # ── Weapons & Skills ──────────────────────────────────────────────────────

    def equip_weapon(self, weapon: Weapon) -> bool:
        """
        Equip a weapon (max 3 slots).

        Returns:
            True if equipped; False if weapon slots are full.
        """
        success = self.weapons.add(weapon)
        if success:
            self.combat_log.append(
                f"{self.name} equipped {weapon.name}"
            )
        return success

    def learn_skill(self, skill: str) -> bool:
        """
        Learn a new skill. set guarantees no duplicates.

        Returns:
            True if new skill; False if already known.
        """
        if not skill or skill in self.skills:
            return False
        self.skills.add(skill)
        return True

    # ── Inventory ─────────────────────────────────────────────────────────────

    def pick_up_item(self, item: Item) -> bool:
        """
        Pick up an item into inventory and register it by type.

        Returns:
            True if added; False if inventory is full.
        """
        success: bool = self.inventory.add(item)
        if success:
            self.combat_log.append(
                f"{self.name} picked up {item.name} ({item.item_type.name})"
            )
        return success


    def items_by_type(self) -> dict[str, list[Item]]:
        """
        Return items grouped by ItemType name as a plain dict copy.
        Callers cannot mutate the internal defaultdict directly.
        """
        items = defaultdict(list)
        
        for item in self.inventory.all():
            items[item.item_type.value].append(item)
        return dict(items)

    # ── Combat & Kill Tracking ────────────────────────────────────────────────

    def record_kill(self, enemy_type: str) -> None:
        """
        Record defeating an enemy.
        Counter accumulates each enemy type; no manual initialization needed.
        """
        self.combat_log.append(f"{self.name} defeated a {enemy_type}")
        self.kill_counts[enemy_type] += 1
        

    def total_damage_potential(self) -> int:
        """Sum damage of all currently equipped weapons."""
        return sum(
            weapon.damage
            for weapon in self.equipped_weapons.all()
            
        )

    def top_kills(self, n: int = 3) -> list[tuple[str, int]]:
        """
        Return the top N most-killed enemy types.
        Counter.most_common() returns them in descending order of count.
        """
        return self.kill_counts.most_common(n)

    # ── Stats ─────────────────────────────────────────────────────────────────

    def upgrade_stat(self, stat: str, amount: int) -> bool:
        """
        Increase a stat by `amount`.

        Returns:
            True if stat exists and was upgraded; False if key not found.
        """
        if stat not in self.stats:
            return False

        self.stats[stat] += amount
        return True
##