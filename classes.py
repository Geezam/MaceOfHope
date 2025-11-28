from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import ui


@dataclass
class Item:
    """
    Represents an item. Using a dataclass for simplicity.
    """
    id: int
    name: str = "Unnamed"
    type: str = "Unknown"
    value: int = 0
    # stats
    hp: int = 0
    spd: int = 0
    eva: int = 0
    dfn: int = 0
    atk: List[int] = field(default_factory=lambda: [0, 0])


@dataclass
class Enemy:
    """
    A base class for an enemy. Using a dataclass
    to auto-generate __init__, __repr__, etc.
    """
    name: str
    lvl: int = 1
    xpG: int = 10
    goldG: int = 10
    dfn: int = 0
    sStats: Dict[str, int] = field(default_factory=lambda: {
        "Health": 5, "Speed": 0, "Evasion": 0
    })
    atk: List[int] = field(default_factory=lambda: [1, 2])
    loot: List['Item'] = field(default_factory=list)


class Hero:
    """
    Represents the player's character.
    All attributes are instance-specific to prevent shared state.
    """
    @staticmethod
    def _hpCalc(vitality: int, proff: str) -> int:
        """Calculates max HP based on vitality and class."""
        hp = vitality * 1.6
        if proff == "Warrior":  # Warriors get extra Health
            hp += 5
        return round(hp)

    @staticmethod
    def _spdCalc(dexterity: int, proff: str) -> int:
        """Calculates speed based on dexterity and class."""
        spd = dexterity * 1.6
        if proff == "Ranger":  # Rangers get extra Speed
            spd += 5
        return round(spd)

    @staticmethod
    def _evaCalc(pStats: Dict[str, int], proff: str) -> int:
        """
    Calculates BASE evasion % as an integer based on all pStats.
    The cap is now applied in the @property.
    """
        BASE_EVASION = 5.0    # 5% base chance

        dex = pStats["Dexterity"]
        intel = pStats["Intelligence"]
        vit = pStats["Vitality"]

        evasion_bonus = (dex * 0.5) + (intel * 0.2) + (vit * 0.1)

        if proff == "Rogue":
            evasion_bonus += 3.0  # Rogues get extra evasion

        calculated_evasion = BASE_EVASION + evasion_bonus

    # Return the raw, uncapped base evasion
        return round(calculated_evasion)

    def __init__(self, name: str, proff: str, affin: str,
                 pstats: Tuple[int, int, int]):
        self.name: str = name
        self.proff: str = proff
        self.affin: str = affin
        self.lvl: int = 1
        self.xp: int = 0
        self.lvlNxt: int = 10
        self.gold: int = 0
        self.inventory: List[Item] = []

        self.pStats: Dict[str, int] = {
            "Vitality": pstats[0],
            "Dexterity": pstats[1],
            "Intelligence": pstats[2]
        }

        # Primary stats
        self.base_hpMax: int = self._hpCalc(self.pStats["Vitality"],
                                            self.proff)
        self.base_speed: int = self._spdCalc(self.pStats["Dexterity"],
                                             self.proff)
        self.base_evasion: int = self._evaCalc(self.pStats,
                                               self.proff)

    # Base stats (from equipment TYPE)
        self.base_atk: List[int] = [1, 2]
        self.base_dfn: int = 0

        self.acc_hp_bonus: int = 0
        self.acc_spd_bonus: int = 0
        self.acc_eva_bonus: int = 0
        self.acc_atk_bonus: List[int] = [0, 0]
        self.acc_dfn_bonus: int = 0

    # Equipment (stores names)
        self.equipment: Dict[str, str] = {"weapon": "unarmed",
                                          "armour": "nekkid",
                                          "accessory": "none"
                                          }

        self.sStats: Dict[str, int] = {"Health": self.base_hpMax}

    @property
    def hpMax(self) -> int:
        """Calculates total Max HP from base + accessory bonus."""
        return self.base_hpMax + self.acc_hp_bonus

    @property
    def dfn(self) -> int:
        """Calculates total defense from armour + accessory."""
        total_dfn = self.base_dfn + self.acc_dfn_bonus
        return total_dfn

    @property
    def atk(self) -> List[int]:
        """Calculates total attack from weapon + accessory."""
        min_atk = self.base_atk[0] + self.acc_atk_bonus[0]
        max_atk = self.base_atk[1] + self.acc_atk_bonus[1]
        return [min_atk, max_atk]

    @property
    def speed(self) -> int:
        """Calculates total speed from base stats + accessory."""
        total_speed = self.base_speed + self.acc_spd_bonus
        return total_speed

    @property
    def evasion(self) -> int:
        """Calculates total evasion from base stats + accessory
        (and applies cap)."""
        total_eva = self.base_evasion + self.acc_eva_bonus

        # Apply hard cap
        MAX_EVASION_CAP = 33.3
        capped_eva = min(total_eva, MAX_EVASION_CAP)

        # Apply floor
        capped_eva = max(capped_eva, 0.0)

        return round(capped_eva)

    def profile(self) -> None:
        """
        Calls the ui module to print the hero's profile.
        This method prints to the console, it does not return a string.
        """
        ui.show_hero_profile(self)
