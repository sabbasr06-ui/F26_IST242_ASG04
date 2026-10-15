"""
models.py
=========
Dataclass definitions for the Hero Quest RPG.
Defines Weapon and Item as lightweight immutable-style data containers.

Imports from:
  enums.py — WeaponType, ItemType

Do not modify.
"""

from dataclasses import dataclass
from hero_rpg.enums import WeaponType, ItemType


@dataclass
class Weapon:
    """
    Represents a weapon the hero can equip.

    Attributes:
        name        : Display name (e.g. "Iron Sword").
        weapon_type : A WeaponType enum value.
        damage      : Base damage dealt per hit.
        durability  : Starts at 100; decreases with use.
    """
    name:        str
    weapon_type: WeaponType
    damage:      int
    durability:  int = 100


@dataclass
class Item:
    """
    Represents any collectible item (potions, armor, misc).

    Attributes:
        name      : Display name (e.g. "Health Potion").
        item_type : An ItemType enum value.
        value     : Gold value of the item.
        quantity  : How many of this item the hero is carrying.
    """
    name:      str
    item_type: ItemType
    value:     int
    quantity:  int = 1
