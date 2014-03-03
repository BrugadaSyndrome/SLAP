import sqlite3

'''
===========
CLASS USAGE
===========
COLOR:
    W  = WHITE
    BL = BLUE
    BK = BLACK
    R  = RED
    G  = GREEN
    C  = COLORLESS
    M  = MULTI-COLORED (USAGE IS 'M-BK/R', LIST HIGHEST COLORED MANA COST FIRST, THEN ALPHABETICALLY)

COST:
    1WWW = ONE GENERAL AND THREE WHITE MANA
    2BRR = ONE BLACK AND TWO RED MANA
    3    = THREE COLORLESS MANA
    X2   = X PLUS 2 MANA AS SPECIFIED ON CARD
    L/G  = ONE LIFE OR GREEN

RARITY:
    C  = COMMON
    U  = UNCOMMON
    R  = RARE
    MR = MYTHIC-RARE

TYPE:
    ARTIFACT
    BASIC LAND
    CREATURE
    ENCHANTMENT
    INSTANT
    LAND
    PLANESWALKER
    SORCERY
    TOKEN
'''

class Card(object):
    def __init__(self):
        #Parts of a card
        self.name = ''
        self.color = ''
        self.cost = ''
        self.card_type = ''
        self.sub_type = ''
        self.expansion_name = ''
        self.rarity = ''
        self.ability_text = ''
        self.reminder_text = ''
        self.flavor_text = ''
        self.power = 0
        self.toughness = 0
        self.painter = ''
        self.expansion_number = 0
        #Extra data
        self.count = 0

    def fill(self, name, color, cost, card_type, sub_type, expansion_name, rarity, ability_text, reminder_text, flavor_text, power, toughness, painter, expansion_number, count):
        #Parts of a card
        self.name = name
        self.color = color
        self.cost = cost
        self.card_type = card_type
        self.sub_type = sub_type
        self.expansion_name = expansion_name
        self.rarity = rarity
        self.ability_text = ability_text
        self.reminder_text = reminder_text
        self.flavor_text = flavor_text
        self.power = power
        self.toughness = toughness
        self.painter = painter
        self.expansion_number = expansion_number
        #Extra data
        self.count = count

def adapt_card(card):
    s  = card.name + ';'
    s += card.color + ';'
    s += card.cost + ';'
    s += card.card_type + ';'
    s += card.sub_type + ';'
    s += card.expansion_name + ';'
    s += card.rarity + ';'
    s += card.ability_text + ';'
    s += card.reminder_text + ';'
    s += card.flavor_text + ';'
    s += str(card.power) + ';'
    s += str(card.toughness) + ';'
    s += card.painter + ';'
    s += str(card.expansion_number) + ';'
    s += str(card.count)
    return s

sqlite3.register_adapter(Card, adapt_card)

con = sqlite3.connect(":memory:")
cur = con.cursor()

e = Card()
c = Card()
c.fill('Frontier Guide', 'G', '1G', 'Creature', 'Elf Scout', '?', 'U', 'blah blah', 'what was that?', 'flavor!', 1, 1, 'Wayne Reynolds', 161, 1)
cur.execute("select ?", (c,))
print cur.fetchone()[0]
