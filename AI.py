import json
import matplotlib.pyplot as plt

with open('steam.json', 'r') as json_file:  # Opent json file onder de naam 'json_file'
    data = json.load(json_file)  # Zet data als alles in de json file, als je data print dan zie je alles in de json

def genres():
    genre_list = set() # Maak een set, zodat het makkelijker is om te checken of data al in de set staat

    for file in data:
        for genre in file["genres"].split(';'):
            genre_list.add(genre.strip())

    return genre_list

def genre_analysis(genre, num_iterations=1000, learning_rate=0.0001):
    # Normaliseer het genre (kleine letters en verwijder spaties)
    normalized_genre = genre.lower().replace(" ", "")

    # Filter spellen op genre
    filtered_data = [
        game for game in data
        if any(g.strip().lower().replace(" ", "").startswith(normalized_genre) for g in game["genres"].split(";"))
    ]

    if not filtered_data:
        print(f"No data available for genre '{genre}'.")
        return None

    # Bereken gemiddelde en mediaan speeltijden
    playtime_list = [game['median_playtime'] for game in filtered_data]
    average_list = [game['average_playtime'] for game in filtered_data]

    if not playtime_list:
        print(f"No playtimes found for the selected genre '{genre}'.")
        return None

    playtime_list.sort()
    average_list.sort()

    gemiddelde = sum(average_list) / len(average_list)
    x = len(playtime_list)
    if x % 2 == 0:
        mediaan = (playtime_list[x // 2 - 1] + playtime_list[x // 2]) / 2
    else:
        mediaan = playtime_list[x // 2]

    # Gradient Descent voor positieve ratings en gemiddelde speeltijd
    positive_ratings = [game['positive_ratings'] for game in filtered_data if game['positive_ratings'] > 0]
    average_playtime = [game['average_playtime'] for game in filtered_data if game['positive_ratings'] > 0]

    if not positive_ratings or not average_playtime:
        print(f"No data for gradient descent analysis in genre '{genre}'.")
        return {"Gemiddelde": gemiddelde, "Mediaan": mediaan}

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

    for _ in range(num_iterations):
        for index in range(n):
            xk = x_scaled[index]
            yk = y_scaled[index]
            error = (a + b * xk) - yk
            a -= error * learning_rate
            b -= xk * error * learning_rate

    a_original = reverse_min_max_scale(a, y_min, y_max)
    b_original = b * (y_max - y_min) / (x_max - x_min)

    # Print resultaten
    print(f"Statistics for Genre '{genre}':")
    print(f"Gemiddelde Speeltijd: {round(gemiddelde,2)}")
    print(f"Mediaan Speeltijd: {round(mediaan,2)}")
    print(f"Gradient Descent Results:")
    print(f"  Intercept (a): {round(a_original,4)}")
    print(f"  Voor elke positieve rating increased de gemiddelde speeltijd met {round(b_original, 4)}")

    # Retourneer alle resultaten in een dictionary
    return {
        "Gemiddelde": gemiddelde,
        "Mediaan": mediaan,
        "Gradient Descent Intercept": a_original,
        "Gradient Descent Slope": b_original,
    }


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


#mediaan_en_gemiddelde()
#search('a')
genre_analysis('casu')
#genre_stats('indi')