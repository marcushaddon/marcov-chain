from random import randint

def weighted_random_choice(weighted_items):
    totalweight = sum([item[0] for item in weighted_items])
    cursor = 0
    threshhold = randint(0, totalweight)
    for item in weighted_items:
        cursor += item[0]
        if cursor >= threshhold:
            return item