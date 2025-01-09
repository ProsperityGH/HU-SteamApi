import json

with open('steam.json', 'r') as json_file:  # Opent json file onder de naam 'json_file'
    data = json.load(json_file)  # Zet data als alles in de json file, als je data print dan zie je alles in de json

def genres():
    genre_list = set() # Maak een set, zodat het makkelijker is om te checken of data al in de set staat

    for file in data:
        for genre in file["genres"].split(';'):
            genre_list.add(genre.strip())

    return genre_list

def genre_stats(genre):
    playtime_list = []
    average_list = []

    # Normaliseer het genre (kleine letters en verwijder spaties)
    normalized_genre = genre.lower().replace(" ", "")

    for game in data:
        # Normaliseer genres van de game
        game_genres = [g.strip().lower().replace(" ", "") for g in game["genres"].split(";")]
        # Controleer of een van de genres begint met de opgegeven zoekterm
        if any(g.startswith(normalized_genre) for g in game_genres):
            playtime_list.append(game['median_playtime'])
            average_list.append(game['average_playtime'])

    if not playtime_list:
        print(f"No playtimes found for the selected genre '{genre}'.")
        return None, None

    # Sorteer de lijsten voor mediane berekening
    playtime_list.sort()
    average_list.sort()

    # Bereken gemiddelde van de gemiddelde playtime
    gemiddelde = sum(average_list) / len(average_list)

    # Bereken de mediaan
    x = len(playtime_list)
    if x % 2 == 0:
        mediaan = (playtime_list[x // 2 - 1] + playtime_list[x // 2]) / 2
    else:
        mediaan = playtime_list[x // 2]

    # Print resultaten
    play_time_list = [gemiddelde,mediaan]
    return mediaan, gemiddelde


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
genre_stats('indi')
