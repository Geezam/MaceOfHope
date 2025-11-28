from classes import Item

# --- TIER 1 WEAPONS: "RUSTY" ---
# (min + max = 8)
knife = Item(id=100, name="Rusty Knife", type="weapon", atk=[0, 8])
sword = Item(id=101, name="Rusty Sword", type="weapon", atk=[1, 7])
mace = Item(id=102, name="Rusty Mace", type="weapon", atk=[2, 6])
spear = Item(id=103, name="Rusty Spear", type="weapon", atk=[3, 5])
axe = Item(id=104, name="Rusty Axe", type="weapon", atk=[4, 4])

rusty_weapons = (knife, sword, mace, spear, axe)

# --- TIER 2 WEAPONS: "IRON" ---
# (min + max = 16)
knife2 = Item(id=110, name="Iron Knife", type="weapon", atk=[0, 16])
sword2 = Item(id=111, name="Iron Sword", type="weapon", atk=[2, 14])
mace2 = Item(id=112, name="Iron Mace", type="weapon", atk=[4, 12])
spear2 = Item(id=113, name="Iron Spear", type="weapon", atk=[6, 10])
axe2 = Item(id=114, name="Iron Axe", type="weapon", atk=[8, 8])

iron_weapons = (knife2, sword2, mace2, spear2, axe2)

# --- TIER 3 WEAPONS: "STEEL" ---
# (min + max = 32)
knife3 = Item(id=120, name="Steel Knife", type="weapon", atk=[0, 32])
sword3 = Item(id=121, name="Steel Sword", type="weapon", atk=[4, 28])
mace3 = Item(id=122, name="Steel Mace", type="weapon", atk=[8, 24])
spear3 = Item(id=123, name="Steel Spear", type="weapon", atk=[12, 20])
axe3 = Item(id=124, name="Steel Axe", type="weapon", atk=[16, 16])

steel_weapons = (knife3, sword3, mace3, spear3, axe3)

# --- TIER 1 ARMOUR: "FABRIC" ---
vest = Item(id=200, name="Fabric Vest", type="armour", dfn=2)

# --- TIER 2 ARMOUR: "LEATHER" ---
vest2 = Item(id=210, name="Leather Vest", type="armour", dfn=4)

# --- TIER 3 ARMOUR: "RIGID" ---
vest3 = Item(id=210, name="Rigid Vest", type="armour", dfn=8)

armour = (vest, vest2, vest3)


# accessories

# treasure
# --- TIER 1 TREASURE: "STONE" ---
statue = Item(id=400, name="Stone Statue", type="Treasure", value=11)
# --- TIER 2 TREASURE: "PLATINUM" ---
statue2 = Item(id=410, name="Platinum Statue", type="Treasure", value=22)
# --- TIER 3 TREASURE: "RUBY" ---
statue3 = Item(id=420, name="Ruby Statue", type="Treasure", value=33)

treasure = (statue, statue2, statue3)

# chests
