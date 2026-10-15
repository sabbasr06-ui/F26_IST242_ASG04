"""
enums.py
========
Enum definitions for the Hero Quest RPG.
Contains all fixed category types used across the project.
Do not modify.
"""

from enum import Enum


class WeaponType(Enum):
    """All possible weapon categories in the game."""
    SWORD  = "Sword"
    BOW    = "Bow"
    STAFF  = "Staff"
    DAGGER = "Dagger"


class ItemType(Enum):
    """All possible item categories that can be picked up."""
    WEAPON = "Weapon"
    POTION = "Potion"
    ARMOR  = "Armor"
    MISC   = "Misc"
