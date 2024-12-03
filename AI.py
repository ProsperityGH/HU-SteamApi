import json,random

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
        game_lst = []
        if game_name == game['name']:          # Als hij de game in de file tegenkomt, bereken dan het percentage van de reviews
            print(f'Game: {game['name']}')
            positive = game['positive_ratings']
            negative = game['negative_ratings']
            game_lst.append(positive), game_lst.append(negative)
            no_brackets = str(game_lst)[1:-1]
            percentage = (positive / (negative+positive)) * 100
            print(f'Like to dislike ratio = {no_brackets.replace(',', ' -')} ({round(percentage,2)}%)')

like_to_dislike(random_game())