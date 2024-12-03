import json
import random

with open('steam.json', 'r') as json_file:
    data = json.load(json_file)


def random_game():
    '''
    Stop elke game in de json file in een lijst, en return dan een random item uit de lijst
    '''
    gamelist = [game['name'] for game in data]  # Genereer lijst van game namen
    rand = random.randint(0, len(gamelist) - 1)  # Kies een random index
    return gamelist[rand]


def like_to_dislike(game_name):
    for game in data:
        if game_name == game['name']:  # Zoek de game
            print(f'Game: {game["name"]}')
            positive = game['positive_ratings']
            negative = game['negative_ratings']

            # Controleer op zero division error
            total_ratings = positive + negative
            if total_ratings == 0:
                print("Geen beoordelingen beschikbaar.")
                return  # Stop de functie als er geen beoordelingen zijn
            percentage = (positive / total_ratings) * 100
            print(f'Like to dislike ratio = {positive} - {negative} ({round(percentage, 2)}%)')


# Gebruik de functies
game = random_game()
like_to_dislike(game)
