import json,random
from math import expm1
from re import search

with open('steam.json', 'r') as json_file:  # Opent json file onder de naam 'json_file'
    data = json.load(json_file)  # Zet data als alles in de json file, als je data print dan zie je alles in de json

def random_game():
    '''''
    Stop elke game in de json file in een lst, en return dan een random item uit de list
    '''''
    gamelist = []
    for game in data:
        gamelist.append(game['name'])
    rand = random.randint(0, len(gamelist)+1)
    return gamelist[rand]


def like_to_dislike(game_name):

    for game in data:                          # Doorloopt elke game in de json
        if game_name == game['name']:          # Als hij de game in de file tegenkomt, bereken dan het percentage van de reviews
            print(f'Game: {game['name']}')
            positive = game['positive_ratings']
            negative = game['negative_ratings']
            percentage = (positive / (negative+positive)) * 100
            print(f'Like to dislike ratio = {positive} - {negative} ({round(percentage,2)}%)')
            break

like_to_dislike(random_game())

def item_search():
    game_list = []
    swapped = True
    while True:
        try:
            search = str(input("Search for a game: "))
            break
        except:
            print('Invalid input, try again.')

    for game in data:
        if search in game['name']:
            game_list.append(game['name'])

    n = len(game_list)
    while swapped:
        swapped = False
        for i in range(n - 1):
            if game_list[i] > game_list[i + 1]:
                game_list[i], game_list[i + 1] = game_list[i + 1], game_list[i]
                swapped = True

    print(game_list)

item_search()