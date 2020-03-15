from lib import shortname
from collections import defaultdict

def parse_card_name(raw_string):
    out = raw_string.split('|')[-1].rstrip('}')
    return out

def parse_expansion(raw_string):
    if '1E' in raw_string:
        if 'Base' in raw_string:
            return 'base_1e'
        else:
            return 'intrigue_1e'
    out = raw_string.lstrip('[').split(']')[0]
    if '|' in out:
        out = out.split('|')[-1]
    return shortname(out)

def parse_types(raw_string):
    types = raw_string.split('-')
    return [shortname(t) for t in types]

def parse_cost(raw_string):
    tokens = raw_string.split('|')
    if len(tokens) <= 2:
        return None
    coins_and_potions = tokens[2].rstrip('}')

    coins = int('0' + coins_and_potions.rstrip('P*+'))
    potions = coins_and_potions.count('P')
    debt = int(tokens[4].rstrip('}')) if len(tokens) > 3 else 0

    return (coins, potions, debt)

def in_supply(card_name, types, card_text):
    if 'not in the supply' in card_text.lower():
        return False
    base_cards = ['estate','duchy','province','colony','potion',
            'copper','silver', 'gold', 'platinum', 'curse']
    split_pile_bottoms = ['avanto', 'rocks', 'fortune',
            'bustling_village', 'emporium', 'plunder']
    if shortname(card_name) in base_cards + split_pile_bottoms:
        return False
    if 'sir_' in shortname(card_name) or 'dame_' in shortname(card_name) or 'castle' in shortname(card_name):
        return False

    for t in types:
        if t in ['heirloom', 'shelter', 'ruins', 'prize', 'spirit', 'zombie']:
            return False

    for t in types:
        if t in ['action', 'victory', 'treasure', 'night']:
            return True
    return False

def format_cost(cost):
    if cost is None:
        return '-'
    coins, potions, debt = cost
    out = str(coins) if coins else ''
    out += 'P' * potions
    if debt:
        if out:
            out += ' '
        out += str(debt) + '⬡'
    return out

cards_by = defaultdict(lambda : defaultdict(list))

cards_by['misc']['randomizable'] = ['knights', 'castles']

with open('raw_data/list_of_cards.raw') as f:
    for line in f:
        tokens = [s.strip().strip('|') for s in line.split('||')]

        card_name = parse_card_name(tokens[0])
        expansion = parse_expansion(tokens[1])
        types = parse_types(tokens[2])
        total_cost = parse_cost(tokens[3])
        card_text = tokens[4]

        if total_cost is not None:
            coins, potions, debt = total_cost
            if potions > 0:
                cards_by['cost']['potion'].append(card_name)
            else:
                cost = coins + debt
                if cost <= 5:
                    cards_by['cost'][str(cost)].append(card_name)
                else:
                    cards_by['cost']['6_plus'].append(card_name)

        cards_by['expansion'][expansion].append(card_name)

        for t in types:
            cards_by['type'][t].append(card_name)

        if in_supply(card_name, types, card_text):
            cards_by['misc']['randomizable'].append(card_name)

for prefix, dictionary in cards_by.items():
    for label, cards in dictionary.items():
        filename = f'tags/{prefix}/{label}.dat'
        with open(filename, 'w') as f:
            f.write('\n'.join(sorted(map(shortname, cards))) + '\n')
