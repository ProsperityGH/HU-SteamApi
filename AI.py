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
        return str(f'De mediaan van de playtime is {((playtime_list[y-1] + playtime_list[y]) / 2)} en de gemiddelde playtime is {round(gemiddelde, 2)}')
    else:
        return str(f'De mediaan van de playtime is {float(playtime_list[int(y)])} en de gemiddelde playtime is {round(gemiddelde, 2)}')

def search(letter):
    gamelist = []
    swapped = True

    normalized_letter = letter.lower().replace(" ", "")

    for game in data:
        normalized_name = game["name"].lower().replace(" ", "")
        if normalized_letter in normalized_name:
            gamelist.append(game["name"])

    while swapped:
        swapped = False
        for i in range(len(gamelist)-1):
            if gamelist[i] > gamelist[i+1]:
                gamelist[i], gamelist[i + 1] = gamelist[i+1], gamelist[i]
                swapped = True

    return gamelist

def genre_search(genre):
    gamelist = []
    swapped = True

    # Loop door alle games in de data
    for game in data:
        # Controleer of het gegeven genre voorkomt in de genres van de game
        if genre in game["genres"].split(";"):
            gamelist.append(game["name"])

    # Sorteer de lijst van games alfabetisch
    while swapped:
        swapped = False
        for i in range(len(gamelist)-1):
            if gamelist[i] > gamelist[i+1]:
                gamelist[i], gamelist[i + 1] = gamelist[i+1], gamelist[i]
                swapped = True

    print(gamelist)
    return gamelist

def gradient_descent(num_iterations=1000, learning_rate=0.0001):
    """Performs gradient descent on positive ratings and average playtime."""
    # Filter out games with 0 positive ratings
    filtered_data = [game for game in data if game['positive_ratings'] > 0]

    positive_ratings = [game['positive_ratings'] for game in filtered_data]
    average_playtime = [game['average_playtime'] for game in filtered_data]

    def min_max_scale(values):
        min_val = min(values)
        max_val = max(values)
        scaled_values = [(val - min_val) / (max_val - min_val) for val in values]
        return scaled_values, min_val, max_val

    def reverse_min_max_scale(value, min_val, max_val):
        return value * (max_val - min_val) + min_val

    x_scaled, x_min, x_max = min_max_scale(positive_ratings)
    y_scaled, y_min, y_max = min_max_scale(average_playtime)

    a = 0
    b = 0
    n = len(x_scaled)

    a_values = []  # To track the intercept over iterations
    b_values = []  # To track the slope over iterations

    for _ in range(num_iterations):
        for index in range(n):
            xk = x_scaled[index]
            yk = y_scaled[index]
            error = (a + b * xk) - yk
            a -= error * learning_rate
            b -= xk * error * learning_rate
        a_values.append(a)
        b_values.append(b)

    # Revert intercept and slope using the integrated reverse function
    a_original = reverse_min_max_scale(a, y_min, y_max)
    b_original = b * (y_max - y_min) / (x_max - x_min)

    print("Gradient Descent Results:")
    print(f"Intercept (a): {a_original}")
    print(f"Voor elke positive rating increased de average playtime met {round(b_original, 4)}")

    return a_original, b_original

#mediaan_en_gemiddelde()
#search('a')
#gradient_descent()
genre_search('Casual')
