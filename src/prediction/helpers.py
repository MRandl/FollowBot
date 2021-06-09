categories_and_keywords = [
    ('has_chain', ['⛓', 'chain']),
    ('has_wave', ['🌊']),
    ('has_100', ['100', '99.5%', '💯']),
    ('has_followback', ['follo', 'フォロ', 'فالو', 'f4f', 'siguemeytesigo', 'تابعني_اتابعك ', '相互希望', 'FB', 'φολλοου']),
    ('has_corona', ['corona', 'virus', 'covid']),
    ('has_bot', ['bot']),
    ('has_invitation_link', ['t.me', 'line.me']),
]

where_to_check = [
    'screen_name',
    'name',
    'location',
    'url',
    'description'
]

def check_usr(usr, id, erate):
    found = [False for x in categories_and_keywords]
    for (index, cat_kword) in enumerate(categories_and_keywords):
        if cat_kword[0] == 'has_invitation_link':
            found[index] = check_invitation_link(usr, cat_kword)
        else:
            found[index] = check_keyword(cat_kword, usr)
    found.append(erate)
    found.append(usr.friends_count)
    found.append(usr.followers_count)
    found.insert(0, id)
    found.insert(8,usr.screen_name)
    return found

def check_keyword(cat_kword, usr):
    for checker in where_to_check:
        for keyword in cat_kword[1]:
            if (usr._json[checker] != None) and (keyword in usr._json[checker]):
                return True
    return False


def check_invitation_link(usr, cat_kword):
    entities = usr.entities
    if 'description' in entities.keys():
        urls = entities['description']['urls']
        if len(urls) != 0:
            expanded = urls[0]['expanded_url']
            if expanded is not None:
                for url in cat_kword[1]:
                    if url in expanded:
                        return True
    if 'url' in entities.keys():
        urls = entities['url']['urls']
        if len(urls) != 0:
            expanded = urls[0]['expanded_url']
            if expanded is not None:
                for url in cat_kword[1]:
                    if url in expanded:
                        return True
    return False