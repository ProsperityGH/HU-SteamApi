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


x = []
y = []
zero_ratings_count = 0

# Doorloop de data en voeg waarden toe aan x en y, alleen als positive_ratings > 0.0
for file in data:
    positive_ratings = file.get("positive_ratings")
    average_playtime = file.get("average_playtime")

    if isinstance(positive_ratings, (int, float)) and isinstance(average_playtime, (int, float)):
        if positive_ratings > 0.0:
            # Als positive_ratings > 0, voeg toe aan x en y
            x.append(positive_ratings)
            y.append(average_playtime)
        else:
            # Als positive_ratings == 0, verhoog de teller
            zero_ratings_count += 1

# Normaliseer data om overflow te voorkomen
if x and y:
    max_x = max(x)
    max_y = max(y)
    x = [xi / max_x for xi in x]
    y = [yi / max_y for yi in y]
else:
    print("Geen geldige data om gradient descent uit te voeren.")
    exit()

def gradient_descent(x, y, num_iterations=1000, learning_rate=0.01):
    a = 0
    b = 0
    n = len(x)

    for i in range(num_iterations):
        total_error_a = 0
        total_error_b = 0

        for index in range(n):
            xk = x[index]
            yk = y[index]
            error = (a + b * xk) - yk

            total_error_a += error
            total_error_b += error * xk

        a -= (learning_rate * total_error_a) / n
        b -= (learning_rate * total_error_b) / n

        # Check op nan
        if any(value is None or value != value for value in [a, b]):
            print("Probleem gedetecteerd: a of b is nan.")
            break

    # Zet de resultaten terug naar de originele schaal
    a_original = a * max_y  # Terugrekenen van a naar de oorspronkelijke schaal
    b_original = b * (max_y / max_x)  # Terugrekenen van b naar de oorspronkelijke schaal

    return [a_original, b_original]

# Test gradient descent
result = gradient_descent(x, y)

print("\n### Resultaten van de Gradient Descent ###")
print(f"\nDe gevonden regressielijn is: y = {result[0]:.4f} + {result[1]:.4f} * x")
print(f"De verwachte gemiddelde speeltijd is {result[0]:.4f} minuten wanneer er geen positieve beoordelingen zijn (x = 0).")
print(f"De gemiddelde speeltijd stijgt met {result[1]:.4f} minuten voor elke eenheid toename in het aantal positieve beoordelingen.")
print(f"Aantal games met 0 positieve beoordelingen (aantal overgeslagen games): {zero_ratings_count}")
print(f"Aantal gebruikte games (x > 0): {len(x)}")

# Extra informatie over de gegevens en de normalisatie
print("\n### Extra informatie over de gebruikte data ###")
print(f"Maximale waarde voor positieve beoordelingen (x): {max_x} positieve beoordelingen")
print(f"Maximale waarde voor gemiddelde speeltijd (y): {max_y} minuten")

# print(search(''))
# print(mediaan_en_gemiddelde())