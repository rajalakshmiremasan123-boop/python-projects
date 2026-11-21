import random
import json
import os

# --- CLASSES & SKILLS ---
CLASSES = {
    "1": {"name": "Warrior", "hp": 150, "mana": 40, "attack": 25, "defense": 15, "crit_chance": 10, "crit_dmg": 150},
    "2": {"name": "Mage", "hp": 100, "mana": 120, "attack": 30, "defense": 5, "crit_chance": 15, "crit_dmg": 170},
    "3": {"name": "Archer", "hp": 110, "mana": 60, "attack": 22, "defense": 8, "crit_chance": 25, "crit_dmg": 180},
    "4": {"name": "Assassin", "hp": 90, "mana": 50, "attack": 28, "defense": 6, "crit_chance": 35, "crit_dmg": 200},
}

SKILLS = {
    "Warrior": [
        {"name": "Slash", "mana": 10, "mult": 1.2, "desc": "Powerful slash"},
        {"name": "Shield Bash", "mana": 15, "mult": 1.0, "effect": "stun", "desc": "Stun 2 turns"},
        {"name": "Rage", "mana": 20, "mult": 1.8, "desc": "Unleash rage"},
        {"name": "Earthquake", "mana": 35, "mult": 2.5, "desc": "Earth shake"},
    ],
    "Mage": [
        {"name": "Fireball", "mana": 15, "mult": 1.5, "desc": "Burn enemy"},
        {"name": "Ice Blast", "mana": 20, "mult": 1.3, "effect": "freeze", "desc": "Freeze 1 turn"},
        {"name": "Thunder Strike", "mana": 25, "mult": 2.0, "desc": "Lightning"},
        {"name": "Meteor", "mana": 50, "mult": 3.0, "desc": "Call meteor"},
    ],
    "Archer": [
        {"name": "Multi Shot", "mana": 15, "mult": 1.4, "desc": "3 arrows"},
        {"name": "Poison Arrow", "mana": 20, "mult": 1.2, "effect": "poison", "desc": "Poison 3 turns"},
        {"name": "Explosive Arrow", "mana": 25, "mult": 2.2, "desc": "Explodes"},
        {"name": "Sniper Shot", "mana": 40, "mult": 3.2, "desc": "Deadly shot"},
    ],
    "Assassin": [
        {"name": "Backstab", "mana": 15, "mult": 1.6, "desc": "From behind"},
        {"name": "Smoke Bomb", "mana": 10, "mult": 0.5, "effect": "dodge", "desc": "Dodge next"},
        {"name": "Shadow Strike", "mana": 25, "mult": 2.3, "desc": "Shadow attack"},
        {"name": "Instant Kill", "mana": 60, "mult": 5.0, "effect": "insta", "desc": "15% insta kill"},
    ],
}

WEAPONS = [
    {"name": "Rusty Sword", "atk": 5, "rarity": "Common", "price": 50},
    {"name": "Wooden Staff", "atk": 6, "rarity": "Common", "price": 60},
    {"name": "Old Bow", "atk": 7, "rarity": "Common", "price": 70},
    {"name": "Dagger", "atk": 8, "rarity": "Common", "price": 80},
    {"name": "Iron Sword", "atk": 12, "rarity": "Uncommon", "price": 150},
    {"name": "Steel Axe", "atk": 14, "rarity": "Uncommon", "price": 180},
    {"name": "Longbow", "atk": 15, "rarity": "Uncommon", "price": 200},
    {"name": "Mage Wand", "atk": 16, "rarity": "Uncommon", "price": 220},
    {"name": "Flame Sword", "atk": 22, "rarity": "Rare", "price": 400},
    {"name": "Frost Staff", "atk": 24, "rarity": "Rare", "price": 450},
    {"name": "Thunder Bow", "atk": 26, "rarity": "Rare", "price": 500},
    {"name": "Shadow Blade", "atk": 28, "rarity": "Rare", "price": 550},
    {"name": "Dragon Slayer", "atk": 35, "rarity": "Epic", "price": 900},
    {"name": "Phoenix Staff", "atk": 38, "rarity": "Epic", "price": 1000},
    {"name": "Elven Bow", "atk": 40, "rarity": "Epic", "price": 1100},
    {"name": "Demon Dagger", "atk": 42, "rarity": "Epic", "price": 1200},
    {"name": "Excalibur", "atk": 55, "rarity": "Legendary", "price": 2000},
    {"name": "Staff of Eldoria", "atk": 60, "rarity": "Legendary", "price": 2500},
    {"name": "Bow of Eternity", "atk": 62, "rarity": "Legendary", "price": 2600},
    {"name": "Soul Reaper", "atk": 65, "rarity": "Legendary", "price": 3000},
    {"name": "Ancient Demon Blade", "atk": 80, "rarity": "Mythic", "price": 5000},
]

ARMORS = [
    {"name": "Leather Vest", "def": 5, "rarity": "Common", "price": 50},
    {"name": "Mage Robe", "def": 6, "rarity": "Common", "price": 80},
    {"name": "Iron Chainmail", "def": 8, "rarity": "Common", "price": 100},
    {"name": "Hunter Jacket", "def": 7, "rarity": "Uncommon", "price": 150},
    {"name": "Steel Plate", "def": 12, "rarity": "Uncommon", "price": 250},
    {"name": "Enchanted Robe", "def": 10, "rarity": "Rare", "price": 350},
    {"name": "Dragon Scale", "def": 18, "rarity": "Rare", "price": 500},
    {"name": "Shadow Cloak", "def": 15, "rarity": "Epic", "price": 700},
    {"name": "Phoenix Armor", "def": 22, "rarity": "Epic", "price": 900},
    {"name": "Armor of Eldoria", "def": 30, "rarity": "Legendary", "price": 1500},
    {"name": "Demon Lord Plate", "def": 35, "rarity": "Legendary", "price": 2000},
    {"name": "Divine Aegis", "def": 45, "rarity": "Mythic", "price": 3500},
]

POTIONS = [
    {"name": "Small HP Potion", "type": "hp", "val": 50, "price": 30},
    {"name": "Medium HP Potion", "type": "hp", "val": 100, "price": 60},
    {"name": "Large HP Potion", "type": "hp", "val": 250, "price": 120},
    {"name": "Giant HP Potion", "type": "hp", "val": 500, "price": 200},
    {"name": "Ultimate HP Potion", "type": "hp", "val": 9999, "price": 400},
    {"name": "Small Mana Potion", "type": "mana", "val": 30, "price": 30},
    {"name": "Medium Mana Potion", "type": "mana", "val": 75, "price": 60},
    {"name": "Large Mana Potion", "type": "mana", "val": 150, "price": 120},
    {"name": "Giant Mana Potion", "type": "mana", "val": 300, "price": 200},
    {"name": "Ultimate Mana Potion", "type": "mana", "val": 9999, "price": 400},
    {"name": "Mixed Potion Small", "type": "mixed", "val": 50, "price": 80},
    {"name": "Mixed Potion Large", "type": "mixed", "val": 200, "price": 180},
    {"name": "Attack Buff Potion", "type": "buff_atk", "val": 20, "price": 150},
    {"name": "Defense Buff Potion", "type": "buff_def", "val": 15, "price": 150},
    {"name": "Crit Buff Potion", "type": "buff_crit", "val": 15, "price": 200},
    {"name": "Elixir of Life", "type": "mixed", "val": 500, "price": 500},
]

ENEMIES = [
    {"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "exp": 20, "gold": 15},
    {"name": "Slime", "hp": 25, "atk": 6, "def": 1, "exp": 15, "gold": 10},
    {"name": "Wolf", "hp": 40, "atk": 12, "def": 3, "exp": 25, "gold": 20},
    {"name": "Skeleton", "hp": 45, "atk": 14, "def": 4, "exp": 30, "gold": 25},
    {"name": "Orc", "hp": 60, "atk": 16, "def": 5, "exp": 35, "gold": 30},
    {"name": "Spider", "hp": 35, "atk": 10, "def": 2, "exp": 22, "gold": 18},
    {"name": "Bandit", "hp": 50, "atk": 13, "def": 3, "exp": 28, "gold": 35},
    {"name": "Zombie", "hp": 55, "atk": 11, "def": 4, "exp": 30, "gold": 20},
    {"name": "Harpy", "hp": 48, "atk": 15, "def": 3, "exp": 32, "gold": 28},
    {"name": "Lizardman", "hp": 70, "atk": 18, "def": 6, "exp": 40, "gold": 35},
    {"name": "Wraith", "hp": 65, "atk": 20, "def": 5, "exp": 45, "gold": 40},
    {"name": "Minotaur", "hp": 90, "atk": 22, "def": 8, "exp": 55, "gold": 50},
    {"name": "Troll", "hp": 110, "atk": 24, "def": 10, "exp": 65, "gold": 60},
    {"name": "Dark Elf", "hp": 80, "atk": 26, "def": 7, "exp": 60, "gold": 55},
    {"name": "Golem", "hp": 130, "atk": 20, "def": 15, "exp": 70, "gold": 45},
    {"name": "Vampire Bat", "hp": 60, "atk": 22, "def": 5, "exp": 50, "gold": 40},
    {"name": "Witch", "hp": 75, "atk": 28, "def": 6, "exp": 65, "gold": 70},
    {"name": "Ogre", "hp": 120, "atk": 26, "def": 9, "exp": 70, "gold": 65},
    {"name": "Basilisk", "hp": 100, "atk": 30, "def": 10, "exp": 75, "gold": 70},
    {"name": "Dark Knight", "hp": 140, "atk": 32, "def": 12, "exp": 85, "gold": 80},
    {"name": "Necromancer", "hp": 110, "atk": 35, "def": 8, "exp": 90, "gold": 90},
    {"name": "Chimera", "hp": 160, "atk": 34, "def": 13, "exp": 95, "gold": 85},
    {"name": "Wyvern", "hp": 180, "atk": 36, "def": 14, "exp": 100, "gold": 100},
    {"name": "Demon Hound", "hp": 130, "atk": 38, "def": 10, "exp": 100, "gold": 95},
    {"name": "Abyss Walker", "hp": 200, "atk": 40, "def": 15, "exp": 120, "gold": 120},
    {"name": "Shadow Beast", "hp": 220, "atk": 45, "def": 18, "exp": 130, "gold": 130},
    {"name": "Elder Dragon Pup", "hp": 250, "atk": 50, "def": 20, "exp": 150, "gold": 150},
]

BOSSES = [
    {"name": "Goblin King", "hp": 200, "atk": 25, "def": 10, "exp": 200, "gold": 200, "lvl": 10},
    {"name": "Forest Guardian", "hp": 350, "atk": 35, "def": 15, "exp": 400, "gold": 400, "lvl": 20},
    {"name": "Cave Troll Lord", "hp": 500, "atk": 45, "def": 20, "exp": 600, "gold": 600, "lvl": 30},
    {"name": "Dark Sorcerer", "hp": 650, "atk": 55, "def": 18, "exp": 800, "gold": 800, "lvl": 40},
    {"name": "Demon General", "hp": 800, "atk": 65, "def": 25, "exp": 1000, "gold": 1000, "lvl": 50},
    {"name": "Ice Dragon", "hp": 1000, "atk": 75, "def": 30, "exp": 1500, "gold": 1500, "lvl": 60},
    {"name": "Lord of Shadows", "hp": 1300, "atk": 85, "def": 35, "exp": 2000, "gold": 2000, "lvl": 70},
    {"name": "Fire Titan", "hp": 1600, "atk": 95, "def": 40, "exp": 2500, "gold": 2500, "lvl": 80},
    {"name": "Void Emperor", "hp": 2000, "atk": 110, "def": 50, "exp": 3500, "gold": 3500, "lvl": 90},
    {"name": "Ancient Demon King", "hp": 3000, "atk": 130, "def": 60, "exp": 5000, "gold": 10000, "lvl": 100},
]

class Player:
    def __init__(self, name, cls):
        c = CLASSES[cls]
        self.name = name
        self.class_name = c["name"]
        self.level = 1
        self.exp = 0
        self.exp_next = 100
        self.max_hp = c["hp"]
        self.hp = self.max_hp
        self.max_mana = c["mana"]
        self.mana = self.max_mana
        self.base_atk = c["attack"]
        self.base_def = c["defense"]
        self.crit = c["crit_chance"]
        self.crit_dmg = c["crit_dmg"]
        self.gold = 100
        self.weapon = None
        self.armor = None
        self.inventory = []
        self.potions = []
        self.bosses = 0
        self.enemies = 0
        self.weapons_col = 0
        self.rare = 0

    @property
    def atk(self):
        return self.base_atk + (self.weapon["atk"] if self.weapon else 0)

    @property
    def df(self):
        return self.base_def + (self.armor["def"] if self.armor else 0)

    def level_up(self, exp_gain):
        self.exp += exp_gain
        while self.exp >= self.exp_next:
            self.exp -= self.exp_next
            self.level += 1
            self.exp_next = int(self.exp_next * 1.5)
            self.max_hp += 15
            self.hp = self.max_hp
            self.max_mana += 10
            self.mana = self.max_mana
            self.base_atk += 3
            self.base_def += 2
            print(f"\n*** LEVEL UP! Level {self.level} ***")

    def save(self):
        try:
            with open("savegame.json", "w") as f:
                json.dump(self.__dict__, f, indent=2)
            print("Game Saved to savegame.json!")
        except Exception as e:
            print(f"Save failed: {e}")

    @staticmethod
    def load():
        try:
            if not os.path.exists("savegame.json"):
                print("No save file found!")
                return None
            with open("savegame.json", "r") as f:
                data = json.load(f)
            p = Player.__new__(Player)
            p.__dict__.update(data)
            print(f"Welcome back {p.name} Lv {p.level}")
            return p
        except Exception as e:
            print(f"Load failed: {e}")
            return None

def calc_dmg(atk, df, crit_chance, crit_mult, defending=False):
    base = max(1, atk - df // 2)
    base = random.randint(int(base * 0.8), int(base * 1.2))
    is_crit = random.randint(1, 100) <= crit_chance
    if is_crit:
        base = int(base * (crit_mult / 100))
    if defending:
        base //= 2
    return base, is_crit

def battle(player, enemy, is_boss=False):
    print("\n" + "="*50)
    print(f"BATTLE: {enemy['name']} {'[BOSS]' if is_boss else ''}")
    print(f"Enemy HP {enemy['hp']} ATK {enemy['atk']} DEF {enemy['def']}")
    print("="*50)
    defending = False
    stun = 0
    poison = 0
    buff_atk = 0
    buff_def = 0
    buff_crit = 0
    buff_turn = 0

    while player.hp > 0 and enemy["hp"] > 0:
        print(f"\nYour HP {player.hp}/{player.max_hp} Mana {player.mana}/{player.max_mana} | Enemy HP {enemy['hp']}/{enemy.get('max_hp', enemy['hp'])}")
        print("1 Attack 2 Skills 3 Heal(20 mana) 4 Potion 5 Defend 6 Stats 7 Run")
        ch = input("> ").strip()

        if ch == "1":
            dmg, crit = calc_dmg(player.atk + buff_atk, enemy["def"], player.crit + buff_crit, player.crit_dmg, False)
            enemy["hp"] -= dmg
            print(f"You deal {dmg} {'CRITICAL!' if crit else ''}")
            defending = False

        elif ch == "2":
            skills = SKILLS[player.class_name]
            for i, s in enumerate(skills, 1):
                print(f"{i}. {s['name']} Mana {s['mana']} x{s['mult']} - {s['desc']}")
            sc = input("Skill num 0 back > ").strip()
            if not sc.isdigit() or int(sc) == 0:
                continue
            sc = int(sc) - 1
            if sc < 0 or sc >= len(skills):
                continue
            s = skills[sc]
            if player.mana < s["mana"]:
                print("No mana!")
                continue
            player.mana -= s["mana"]
            eff = s.get("effect")
            dmg = int(player.atk * s["mult"])
            if eff == "stun":
                stun = 2
                enemy["hp"] -= dmg
                print(f"{s['name']} stuns! {dmg} dmg")
            elif eff == "freeze":
                stun = 1
                enemy["hp"] -= dmg
                print(f"{s['name']} freezes! {dmg}")
            elif eff == "poison":
                poison = 3
                enemy["hp"] -= dmg
                print(f"{s['name']} poisons! {dmg}")
            elif eff == "dodge":
                defending = True
                print("You will dodge next!")
            elif eff == "insta":
                if random.random() < 0.15:
                    enemy["hp"] = 0
                    print("INSTANT KILL SUCCESS!")
                else:
                    enemy["hp"] -= dmg
                    print(f"{s['name']} {dmg} dmg but insta fail")
            else:
                enemy["hp"] -= dmg
                print(f"{s['name']} deals {dmg}!")

        elif ch == "3":
            if player.mana < 20:
                print("Need 20 mana")
                continue
            player.mana -= 20
            heal = 30 + player.level * 5
            player.hp = min(player.max_hp, player.hp + heal)
            print(f"Healed {heal} HP")

        elif ch == "4":
            if not player.potions:
                print("No potions")
                continue
            for i, p in enumerate(player.potions, 1):
                print(f"{i}. {p['name']}")
            pc = input("Use num 0 back > ").strip()
            if not pc.isdigit() or int(pc) == 0:
                continue
            pot = player.potions.pop(int(pc) - 1)
            t = pot["type"]
            v = pot["val"]
            if t == "hp":
                player.hp = min(player.max_hp, player.hp + (player.max_hp if v >= 9999 else v))
                print(f"HP restored {v}")
            elif t == "mana":
                player.mana = min(player.max_mana, player.mana + (player.max_mana if v >= 9999 else v))
                print(f"Mana restored {v}")
            elif t == "mixed":
                player.hp = min(player.max_hp, player.hp + v)
                player.mana = min(player.max_mana, player.mana + v)
                print(f"HP+Mana {v}")
            else:
                if "atk" in t:
                    buff_atk = v
                    buff_turn = 3
                    print(f"ATK +{v} 3 turns")
                elif "def" in t:
                    buff_def = v
                    buff_turn = 3
                    print(f"DEF +{v} 3 turns")
                elif "crit" in t:
                    buff_crit = v
                    buff_turn = 3
                    print(f"CRIT +{v}% 3 turns")

        elif ch == "5":
            defending = True
            print("Defending 50% reduction")
        elif ch == "6":
            print(f"{player.name} Lv{player.level} ATK {player.atk} DEF {player.df} Gold {player.gold}")
            continue
        elif ch == "7":
            if is_boss:
                print("Cannot run from boss!")
                continue
            if random.random() < 0.6:
                print("Ran away!")
                return True, False
            else:
                print("Run failed!")
        else:
            continue

        if enemy["hp"] <= 0:
            break
        if poison > 0:
            pd = 10 + player.level * 2
            enemy["hp"] -= pd
            print(f"Poison {pd} dmg")
            poison -= 1
        if stun > 0:
            print(f"{enemy['name']} stunned skips!")
            stun -= 1
        else:
            dmg, _ = calc_dmg(enemy["atk"], player.df + buff_def, 5, 150, defending)
            player.hp -= dmg
            print(f"Enemy attacks {dmg}! Your HP {player.hp}")
            defending = False
        if buff_turn > 0:
            buff_turn -= 1
            if buff_turn == 0:
                buff_atk = 0
                buff_def = 0
                buff_crit = 0

    if player.hp <= 0:
        print("\n*** YOU DIED - GAME OVER ***")
        return False, True
    else:
        print(f"\n*** Defeated {enemy['name']}! +{enemy['exp']} EXP +{enemy['gold']} Gold ***")
        player.level_up(enemy["exp"])
        player.gold += enemy["gold"]
        player.enemies += 1
        if is_boss:
            player.bosses += 1
        if random.random() < 0.3:
            p = random.choice(POTIONS)
            player.potions.append(p)
            print(f"Loot: {p['name']}")
        if random.random() < 0.2:
            w = random.choice(WEAPONS[:10])
            player.inventory.append(w)
            player.weapons_col += 1
            print(f"Found weapon: {w['name']}")
        return True, False

def shop(player):
    while True:
        print(f"\n--- SHOP Gold {player.gold} --- 1 Weapons 2 Armor 3 Potions 4 Sell 5 Exit")
        c = input("> ").strip()
        if c == "1":
            for i, w in enumerate(WEAPONS, 1):
                print(f"{i}. {w['name']} [{w['rarity']}] ATK {w['atk']} {w['price']}G")
            b = input("Buy num 0 back > ").strip()
            if b.isdigit() and int(b) != 0:
                idx = int(b) - 1
                if 0 <= idx < len(WEAPONS) and player.gold >= WEAPONS[idx]["price"]:
                    player.gold -= WEAPONS[idx]["price"]
                    player.inventory.append(WEAPONS[idx])
                    print("Bought!")
                else:
                    print("Not enough gold!")
        elif c == "2":
            for i, a in enumerate(ARMORS, 1):
                print(f"{i}. {a['name']} DEF {a['def']} {a['price']}G")
            b = input("Buy num 0 back > ").strip()
            if b.isdigit() and int(b) != 0:
                idx = int(b) - 1
                if 0 <= idx < len(ARMORS) and player.gold >= ARMORS[idx]["price"]:
                    player.gold -= ARMORS[idx]["price"]
                    player.inventory.append(ARMORS[idx])
                    print("Bought!")
                else:
                    print("Not enough gold!")
        elif c == "3":
            for i, p in enumerate(POTIONS, 1):
                print(f"{i}. {p['name']} {p['price']}G")
            b = input("Buy num 0 back > ").strip()
            if b.isdigit() and int(b) != 0:
                idx = int(b) - 1
                if 0 <= idx < len(POTIONS) and player.gold >= POTIONS[idx]["price"]:
                    player.gold -= POTIONS[idx]["price"]
                    player.potions.append(POTIONS[idx])
                    print("Bought!")
                else:
                    print("Not enough gold!")
        elif c == "4":
            if not player.inventory:
                print("Empty")
                continue
            for i, it in enumerate(player.inventory, 1):
                print(f"{i}. {it['name']}")
            s = input("Sell num 0 back > ").strip()
            if s.isdigit() and int(s) != 0:
                idx = int(s) - 1
                if 0 <= idx < len(player.inventory):
                    it = player.inventory.pop(idx)
                    gain = it["price"] * 60 // 100
                    player.gold += gain
                    print(f"Sold for {gain}")
        elif c == "5":
            break

def inventory_manage(player):
    while True:
        print(f"\n--- INVENTORY Weapon {player.weapon['name'] if player.weapon else 'None'} Armor {player.armor['name'] if player.armor else 'None'} ---")
        for i, it in enumerate(player.inventory, 1):
            print(f"{i}. {it['name']} {it.get('rarity','')}")
        print("1 Equip Weapon 2 Equip Armor 3 Unequip 4 Drop 5 Back")
        c = input("> ").strip()
        if c == "1":
            n = input("Weapon num > ").strip()
            if n.isdigit():
                idx = int(n) - 1
                if 0 <= idx < len(player.inventory) and "atk" in player.inventory[idx]:
                    player.weapon = player.inventory[idx]
                    print(f"Equipped {player.weapon['name']}")
        elif c == "2":
            n = input("Armor num > ").strip()
            if n.isdigit():
                idx = int(n) - 1
                if 0 <= idx < len(player.inventory) and "def" in player.inventory[idx]:
                    player.armor = player.inventory[idx]
                    print(f"Equipped {player.armor['name']}")
        elif c == "3":
            player.weapon = None
            player.armor = None
            print("Unequipped")
        elif c == "4":
            n = input("Drop num > ").strip()
            if n.isdigit():
                idx = int(n) - 1
                if 0 <= idx < len(player.inventory):
                    print(f"Dropped {player.inventory.pop(idx)['name']}")
        elif c == "5":
            break

def get_enemy(level):
    pool = ENEMIES[:min(5 + level, len(ENEMIES))]
    base = random.choice(pool).copy()
    scale = 1 + (level * 0.15)
    base["hp"] = int(base["hp"] * scale)
    base["max_hp"] = base["hp"]
    base["atk"] = int(base["atk"] * (1 + level * 0.08))
    base["def"] = int(base["def"] * (1 + level * 0.05))
    return base

def main():
    while True:
        print("""

LEGENDS OF THE FORGOTTEN REALM

1. New Game
2. Continue (Load)
3. Instructions
4. Exit
""")
        ch = input("> ").strip()
        if ch == "1":
            name = input("Enter Player Name: ").strip() or "Hero"
            print("\nChoose Class:")
            print("1 Warrior (High HP, High Defense)")
            print("2 Mage (High Mana, Magic)")
            print("3 Archer (Balanced, High Crit)")
            print("4 Assassin (Low HP, Very High Crit)")
            cls = input("Choose 1-4 > ").strip()
            if cls not in ["1", "2", "3", "4"]:
                cls = "1"
            player = Player(name, cls)
            print(f"\nWelcome {player.name} the {player.class_name}!")

            while True:
                print(f"\n=== WORLD MAP Lv{player.level} HP{player.hp}/{player.max_hp} Mana{player.mana}/{player.max_mana} Gold{player.gold} Boss {player.bosses}/10 ===")
                print("1 Explore Forest 2 Fight Boss 3 Shop 4 Inventory 5 Stats 6 Save 7 Rest(20G) 8 Exit")
                act = input("> ").strip()
                if act == "1":
                    e = get_enemy(player.level)
                    won, dead = battle(player, e, False)
                    if dead:
                        break
                elif act == "2":
                    need = (player.bosses + 1) * 10
                    if player.level < need:
                        print(f"You need Level {need} to fight next boss! Current {player.level}")
                        continue
                    if player.bosses >= len(BOSSES):
                        print("All bosses defeated! You won!")
                        break
                    boss = BOSSES[player.bosses].copy()
                    boss["max_hp"] = boss["hp"]
                    print(f"\n*** BOSS: {boss['name']} Level {boss['lvl']} ***")
                    if input("Fight Boss? y/n > ").lower() != "y":
                        continue
                    won, dead = battle(player, boss, True)
                    if dead:
                        break
                    if player.bosses >= len(BOSSES):
                        print(f"\nVICTORY! You defeated {boss['name']}! Eldoria saved!\nName {player.name} Level {player.level} Gold {player.gold} Score {player.level*100+player.gold+player.bosses*500}")
                        player.save()
                        break
                elif act == "3":
                    shop(player)
                elif act == "4":
                    inventory_manage(player)
                elif act == "5":
                    print(f"{player.name} {player.class_name} Lv{player.level} EXP {player.exp}/{player.exp_next} ATK {player.atk} DEF {player.df} Gold {player.gold} Crit {player.crit}%")
                elif act == "6":
                    player.save()
                elif act == "7":
                    if player.gold >= 20:
                        player.gold -= 20
                        player.hp = player.max_hp
                        player.mana = player.max_mana
                        print("Rested! HP/Mana full!")
                    else:
                        print("Need 20 Gold!")
                elif act == "8":
                    if input("Save before exit? y/n > ").lower() == "y":
                        player.save()
                    break

        elif ch == "2":
            player = Player.load()
            if not player:
                continue
            while True:
                print(f"\n=== WORLD MAP Lv{player.level} HP{player.hp}/{player.max_hp} Gold{player.gold} Boss {player.bosses}/10 ===")
                print("1 Explore 2 Boss 3 Shop 4 Inventory 5 Stats 6 Save 7 Rest 8 Exit")
                act = input("> ").strip()
                if act == "1":
                    e = get_enemy(player.level)
                    won, dead = battle(player, e, False)
                    if dead:
                        break
                elif act == "2":
                    need = (player.bosses + 1) * 10
                    if player.level < need:
                        print(f"Need Level {need}")
                        continue
                    if player.bosses >= len(BOSSES):
                        print("All bosses done!")
                        break
                    boss = BOSSES[player.bosses].copy()
                    boss["max_hp"] = boss["hp"]
                    if input(f"Fight {boss['name']}? y/n > ").lower() != "y":
                        continue
                    won, dead = battle(player, boss, True)
                    if dead:
                        break
                    if player.bosses >= len(BOSSES):
                        print("VICTORY! Eldoria saved!")
                        player.save()
                        break
                elif act == "3":
                    shop(player)
                elif act == "4":
                    inventory_manage(player)
                elif act == "5":
                    print(f"{player.name} Lv{player.level} ATK {player.atk} DEF {player.df} Gold {player.gold}")
                elif act == "6":
                    player.save()
                elif act == "7":
                    if player.gold >= 20:
                        player.gold -= 20
                        player.hp = player.max_hp
                        player.mana = player.max_mana
                        print("Rested!")
                elif act == "8":
                    if input("Save? y/n > ").lower() == "y":
                        player.save()
                    break

        elif ch == "3":
            print("\nStory: Eldoria darkness, monsters everywhere. Every 10 levels boss guards next region. Defeat all, reach 100, destroy Demon King. Classes Warrior Mage Archer Assassin. Tip: Buy potions before boss! Save often!")
            input("Press Enter...")
        elif ch == "4":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
