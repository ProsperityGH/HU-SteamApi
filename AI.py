import json

with open('steam.json', 'r') as json_file:
    data = json.load(json_file)

for game in data:
    game_lst = []
    print(game['name'])
    positive = game['positive_ratings']
    negative = game['negative_ratings']
    game_lst.append(positive), game_lst.append(negative)
    no_brackets = str(game_lst)[1:-1]

    print(f'Like to dislike ratio = {no_brackets.replace(',', ' -')}')
