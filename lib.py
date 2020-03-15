def shortname(card_name):
    card_name = card_name.lower().strip()

    spacers = [' ', '-']

    for character in set(card_name):
        if not character.isalpha():
            if character in spacers:
                card_name = card_name.replace(character, '_')
            else:
                card_name = card_name.replace(character, '')

    return card_name
