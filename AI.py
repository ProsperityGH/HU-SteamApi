import json

def like_to_dislike(game_name):
    with open('steam.json', 'r') as json_file: # Opent json file onder de naam 'json_file'
        data = json.load(json_file)            # Zet data als alles in de json file, als je data print dan zie je alles in de json

    for game in data:                          # Doorloopt elke game in de json
        game_lst = []
        if game_name == game['name']:
            print(game['name'])
            positive = game['positive_ratings']
            negative = game['negative_ratings']
            game_lst.append(positive), game_lst.append(negative)
            no_brackets = str(game_lst)[1:-1]
            percentage = ((negative-positive) / positive) * -100
            print(f'Like to dislike ratio = {no_brackets.replace(',', ' -')} ({round(percentage,2)}%)')

like_to_dislike('Half-Life: Blue Shift')