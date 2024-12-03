import json

with open('steam.json', 'r') as json_file:  # Opent json file onder de naam 'json_file'
    data = json.load(json_file)  # Zet data als alles in de json file, als je data print dan zie je alles in de json

def mediaan():
    playtime_list = []
    swapped = True

    for median in data:
        playtime_list.append(median['median_playtime'])

    x = len(playtime_list)-1
    y = x / 2

    while swapped:
        swapped = False
        for i in range(x):
            if playtime_list[i] > playtime_list[i+1]:
                playtime_list[i], playtime_list[i+1] = playtime_list[i+1], playtime_list[i]
                swapped = True

    print(playtime_list)
    return playtime_list[int(y)]


def search(letter):
    gamelist = []
    swapped = True

    for game in data:
        if letter in game["name"]:
            gamelist.append(game["name"])

    while swapped:
        swapped = False
        for i in range(len(gamelist)-1):
            if gamelist[i] > gamelist[i+1]:
                gamelist[i], gamelist[i + 1] = gamelist[i+1], gamelist[i]
                swapped = True

    return gamelist

# print(search('b'))
print(mediaan())