from typing import List, Dict, Tuple, Union
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
    # Using lambda to ensure every item has its own attack list
    atk: List[int] = field(default_factory=lambda: [0, 0])


@dataclass
class Enemy:
    """
    A base class for an enemy.
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
    loot: List[Item] = field(default_factory=list)


@dataclass
class Room:
    name: str
    description: str
    image_desc: str
    art: str = "xxx"
    encounter_rate: float = 0.2
    exits: Dict[str, str] = field(default_factory=dict)

    def add_exit(self, direction, room_key):
        self.exits[direction] = room_key


class Hero:
    """
    Represents the player's character.
    Standard class used here to handle complex initialization logic.
    """
    @staticmethod
    def _hpCalc(vitality: int, proff: str) -> int:
        hp = vitality * 1.6
        if proff == "Warrior":
            hp += 5
        return round(hp)

    @staticmethod
    def _spdCalc(dexterity: int, proff: str) -> int:
        spd = dexterity * 1.6
        if proff == "Ranger":
            spd += 5
        return round(spd)

    @staticmethod
    def _evaCalc(pStats: Dict[str, int], proff: str) -> int:
        BASE_EVASION = 5.0
        dex = pStats["Dexterity"]
        intel = pStats["Intelligence"]
        vit = pStats["Vitality"]

        evasion_bonus = (dex * 0.5) + (intel * 0.2) + (vit * 0.1)

        if proff == "Rogue":
            evasion_bonus += 3.0

        return round(BASE_EVASION + evasion_bonus)

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

        # Bonuses applied by functions.equip_item
        self.acc_hp_bonus: int = 0
        self.acc_spd_bonus: int = 0
        self.acc_eva_bonus: int = 0
        self.acc_atk_bonus: List[int] = [0, 0]
        self.acc_dfn_bonus: int = 0

        self.equipment: Dict[str, Union[str, Item]] = {
            "weapon": "unarmed",
            "armour": "nekkid",
            "accessory": "none"
        }

        self.sStats: Dict[str, int] = {"Health": self.base_hpMax}

    @property
    def hpMax(self) -> int:
        return self.base_hpMax + self.acc_hp_bonus

    @property
    def dfn(self) -> int:
        return self.base_dfn + self.acc_dfn_bonus

    @property
    def atk(self) -> List[int]:
        min_atk = self.base_atk[0] + self.acc_atk_bonus[0]
        max_atk = self.base_atk[1] + self.acc_atk_bonus[1]
        return [min_atk, max_atk]

    @property
    def speed(self) -> int:
        return self.base_speed + self.acc_spd_bonus

    @property
    def evasion(self) -> int:
        total_eva = self.base_evasion + self.acc_eva_bonus
        MAX_EVASION_CAP = 33.3  # Apply hard cap
        return round(max(min(total_eva, MAX_EVASION_CAP), 0.0))

    def profile(self) -> None:
        ui.show_hero_profile(self)
