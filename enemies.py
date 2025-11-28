import classes

# Low Level enemies
slime = classes.Enemy(name="Slime", lvl=1, xpG=10, dfn=0, atk=[0, 5],
                      sStats={"Health": 15, "Speed": 1, "Evasion": 1},
                      loot=[])
rat = classes.Enemy(name="Rat", lvl=1, xpG=10, dfn=0, atk=[1, 4],
                    sStats={"Health": 15, "Speed": 1, "Evasion": 1},
                    loot=[])
spider = classes.Enemy(name="Spider", lvl=1, xpG=10, dfn=0, atk=[2, 3],
                       sStats={"Health": 15, "Speed": 1, "Evasion": 1},
                       loot=[])

low_lvl_ene = [slime, rat, spider]

# Mid Level enemies

slime2 = classes.Enemy(name="Massive Slime", lvl=2, xpG=15, dfn=1, atk=[2, 8],
                       sStats={"Health": 25, "Speed": 5, "Evasion": 1},
                       loot=[])
rat2 = classes.Enemy(name="Fat Rat", lvl=2, xpG=15, dfn=1, atk=[3, 7],
                     sStats={"Health": 25, "Speed": 5, "Evasion": 1},
                     loot=[])
spider2 = classes.Enemy(name="Giant Spider", lvl=2, xpG=15, dfn=1, atk=[4, 6],
                        sStats={"Health": 25, "Speed": 5, "Evasion": 1},
                        loot=[])

mid_lvl_ene = [slime2, rat2, spider2]

# High Level enemies


# Bosses (with gimic?)
