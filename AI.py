import json

with open('steam.json', 'r') as json_file:  # Opent json file onder de naam 'json_file'
    data = json.load(json_file)  # Zet data als alles in de json file, als je data print dan zie je alles in de json

def genres():
    genre_list = set() # Maak een set, zodat het makkelijker is om te checken of data al in de set staat

    for file in data:
        for genre in file["genres"].split(';'):
            genre_list.add(genre.strip())

    return genre_list


def mediaan_en_gemiddelde():
    playtime_list = []
    average_list = []

    print(genres())
    genre = str(input(f"Choose a genre from the list above: "))

    for playtime in data:
        if genre in playtime["genres"].split(";"): # Checkt of de gekozen genre in de game zit, zo ja dan word hij aan de lijst toegevoegd
            playtime_list.append(playtime['median_playtime'])
            average_list.append(playtime['average_playtime'])

    if not playtime_list:
        print("No playtimes found for the selected genre.")
        return None, None

    x = len(playtime_list)
    y = x // 2
    swapped = True

    while swapped: # Sorteert de lijst
        swapped = False
        for i in range(x-1): # Sorteer playtime_list
            if playtime_list[i] > playtime_list[i+1]:
                playtime_list[i], playtime_list[i+1] = playtime_list[i+1], playtime_list[i]
                swapped = True
        for e in range(x-1): # Sorteer average_list
            if average_list[e] > average_list[e+1]:
                average_list[e], average_list[e+1] = average_list[e+1], average_list[e]
                swapped = True

    gemiddelde = sum(average_list)/len(average_list)

    if x % 2 == 0:
        # Als de lijst een even getal in lengte is, return dan het midden van de twee middelste getallen
        print(len(playtime_list))
        return ((playtime_list[y-1] + playtime_list[y]) / 2), round(gemiddelde, 2)
    else:
        print(len(playtime_list))
        return float(playtime_list[int(y)]), round(gemiddelde, 2)



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
print(mediaan_en_gemiddelde())