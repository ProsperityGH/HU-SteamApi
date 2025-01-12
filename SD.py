import math
import tkinter as tk
from tkinter import messagebox
import psycopg2
from serial import Serial, STOPBITS_ONE
import AI
import serial
from AI import *
from datetime import datetime
import tkinter as tk

now = datetime.now()
current_time = now.strftime("%H")

#Check of het te laat is om te gamen
if (int(current_time) < 24 and int(current_time) > 6):
    try:
        serialPort = Serial(
            port="COM3",
            baudrate=115200,
            bytesize=8,
            timeout=2,
            stopbits=STOPBITS_ONE
        )
    except Exception as e:
        print("Could not open serial port: " + str(e))
    search_results = []
    current_index = -1
    root = tk.Tk()
    root.title("Gamblers")
    root.attributes('-fullscreen', True)
    root.configure(bg="#F0F0F0")
    nav_menu_frame = tk.Frame(root, bg="#F0F0F0")
    nav_menu_frame.pack(fill="x", side="top")
    content_frame = tk.Frame(root, bg='#F0F0F0')
    content_frame.pack(fill="both", expand=True)
#Homepage
    def Home_Page():
        for widget in content_frame.winfo_children():
            widget.destroy()
        title_label = tk.Label(content_frame, text="Welkom bij de Gamblers!", font=("Helvetica", 40, 'bold'), fg='#4CAF50', bg='#F0F0F0')
        title_label.pack(expand=True)
        description_label = tk.Label(content_frame, text="Dit is onze applicatie, hier kan je steam games opzoeken, statestieken bekijken en nog veel meer!", font=("Helvetica", 20), fg="#333333", bg='#F0F0F0')
        description_label.pack(pady=20)

#Dit is de genre pagina
    def GenrePagina():
        global search_results, current_index
        for widget in content_frame.winfo_children():
            widget.destroy()
        search_label = tk.Label(content_frame, text="Type een genre in om de statestieken van de genre te zien:", font=("Helvetica", 24, "bold"),
                                bg='#F5F5F5')
        search_label.pack(pady=50)
        search_frame = tk.Frame(content_frame, bg='#F5F5F5')
        search_frame.pack(pady=10)
        search_entry = tk.Entry(search_frame, width=40, font=("Helvetica", 18), bd=2, relief="solid", fg="gray")
        search_entry.grid(row=0, column=0, padx=(0, 10))  # Add padding between entry and button
        search_button = tk.Button(search_frame, text="Search", font=("Helvetica", 18), bg="#4CAF50", fg="black",
                                  relief="flat", padx=20, pady=10)
        search_button.grid(row=0, column=1)
        result_frame = tk.Frame(content_frame, bg='#F5F5F5')
        result_frame.pack(pady=20)


        def Zoeken():
            search_term = search_entry.get().strip()
            if not search_term:
                messagebox.showwarning("Input Error", "Please enter a genre name to search.")
                return
            mediaan, gemiddelde = genre_stats(search_term)

            if mediaan is None or gemiddelde is None:
                messagebox.showwarning("No Results", f"No data found for the genre '{search_term}'.")
                return
            for widget in result_frame.winfo_children():
                widget.destroy()
            mediaan_label = tk.Label(result_frame, text=f"Median Playtime: {round(mediaan,1)} minutes",
                                     font=("Helvetica", 24, 'bold'), bg='#F5F5F5')
            mediaan_label.pack(pady=10)
            gemiddelde_label = tk.Label(result_frame, text=f"Average Playtime: {round(gemiddelde,1)} minutes",
                                        font=("Helvetica", 24, 'bold'), bg='#F5F5F5')
            gemiddelde_label.pack(pady=10)
        search_button.config(command=Zoeken)
#Dit is de zoekpagina
    def ZoekPagina():
        global search_results, current_index
        for widget in content_frame.winfo_children():
            widget.destroy()
        search_label = tk.Label(content_frame, text="Enter game name to search:", font=("Helvetica", 24, "bold"), bg='#F5F5F5')
        search_label.pack(pady=50)
        search_entry = tk.Entry(content_frame, width=40, font=("Helvetica", 18), bd=2, relief="solid", fg="gray")
        search_entry.pack(pady=10)
        result_frame = tk.Frame(content_frame, bg='#F5F5F5')
        result_frame.pack(pady=20)
        result_listbox = tk.Listbox(result_frame, height=15, width=50, font=("Helvetica", 18), bg='#FFFFFF', fg='#333333', bd=2, relief="solid", selectmode=tk.SINGLE)
        result_listbox.pack(side="left", fill="y", padx=20)
        scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        result_listbox.config(yscrollcommand=scrollbar.set)
        rating = str("9") + str("\r")
        serialPort.write(str(rating).encode())

        def Zoeken():
            global search_results, current_index
            search_term = search_entry.get().strip()
            if not search_term:
                messagebox.showwarning("Input Error", "Please enter a game name to search.")
                return
            search_results = search(search_term)
            if not search_results:
                messagebox.showinfo("No Results", "No games found with the search term.")
                return
            result_listbox.delete(0, tk.END)
            for game in search_results:
                result_listbox.insert(tk.END, game)
            current_index = 0
            result_listbox.bind("<Double-1>", lambda event: Game_info(result_listbox.get(result_listbox.curselection())))
        search_button = tk.Button(content_frame, text="Search", command=Zoeken, font=("Helvetica", 18), bg="#4CAF50", fg="black", relief="flat", padx=20, pady=10)
        search_button.pack(pady=30)
#Dit laat de game informatie zien
    def Game_info(selected_game):
        i = 0
        for dict in data:
            if dict['name'].lower() == selected_game.lower():
                break
            i = i + 1

        game = data[i]
        zoek_Handle(game['name'])
        for widget in content_frame.winfo_children():
            widget.destroy()
        details_frame = tk.Frame(content_frame, bg='#F5F5F5')
        details_frame.pack(pady=50, padx=20, fill="both", expand=True)
        detail_label = tk.Label(details_frame, text=f"Name: {game['name']}", font=("Helvetica", 18), justify=tk.LEFT, bg='#F5F5F5')
        detail_label.pack(pady=5)
        price_label = tk.Label(details_frame, text=f"Price: {game['price']}", font=("Helvetica", 18), bg='#F5F5F5')
        price_label.pack(pady=5)
        genres_label = tk.Label(details_frame, text=f"Genres: {game['genres']}", font=("Helvetica", 18), bg='#F5F5F5')
        genres_label.pack(pady=5)
        steam_tags_label = tk.Label(details_frame, text=f"Steam Tags: {game['steamspy_tags']}", font=("Helvetica", 18), bg='#F5F5F5')
        steam_tags_label.pack(pady=5)

        try:
            rating = math.ceil(game['positive_ratings']) / (game['positive_ratings'] + game['negative_ratings'])
        except ZeroDivisionError:
            rating = 0
        rating_label = tk.Label(details_frame, text=f"Positive Ratings Ratio: {rating:.2f}", font=("Helvetica", 18), bg='#F5F5F5')
        rating_label.pack(pady=10)
        more_info_button = tk.Button(content_frame, text="More Info", command=lambda: meer_info(game), font=("Helvetica", 16), bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)
        more_info_button.place(relx=0.5, rely=0.92, anchor="s")
        back_button = tk.Button(content_frame, text="Back to Search", command=ZoekPagina, font=("Helvetica", 16), bg="#FF5722", fg="white", relief="flat", padx=20, pady=10)
        back_button.place(relx=0.05, rely=0.05, anchor="nw")
        prev_button = tk.Button(content_frame, text="Previous Game", command=Vorige_pagina, font=("Helvetica", 16), bg="#2196F3", fg="white", relief="flat", padx=20, pady=10)
        prev_button.place(relx=0.05, rely=0.92, anchor="sw")
        next_button = tk.Button(content_frame, text="Next Game", command=Volgende_pagina, font=("Helvetica", 16), bg="#2196F3", fg="white", relief="flat", padx=20, pady=10)
        next_button.place(relx=0.95, rely=0.92, anchor="se")
        pos = game['positive_ratings']
        neg = game['negative_ratings']
        rating = math.ceil(pos / (pos + neg) * 100 / 20)
        rating = str(rating) + str("\r")
        serialPort.write(str(rating).encode())
#Game volgende pagina
    def Volgende_pagina():
        global current_index
        if current_index < len(search_results) - 1:
            current_index += 1
            Game_info(search_results[current_index])
#Game terug functie
    def Vorige_pagina():
        global current_index
        if current_index > 0:
            current_index -= 1
            Game_info(search_results[current_index])
#Dit maakt de meer informatie pagina
    def meer_info(game):
        for widget in content_frame.winfo_children():
            widget.destroy()
        more_info_label = tk.Label(content_frame, text=f"Full Information for {game['name']}\n\n", font=("Helvetica", 20, 'bold'), bg='#F5F5F5')
        more_info_label.pack(padx=20, pady=20)
        info_listbox = tk.Listbox(content_frame, height=15, width=70, font=("Helvetica", 16), bg='#FFFFFF', fg='#333333', bd=2, relief="solid")
        info_listbox.pack(padx=20, pady=20, fill="both", expand=True)
        for key, value in game.items():
            info_listbox.insert(tk.END, f"{key}: {value}")
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=info_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        info_listbox.config(yscrollcommand=scrollbar.set)
        back_button = tk.Button(content_frame, text="Back to Game Details", command=lambda: Game_info(game['name']), font=("Helvetica", 16), bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)
        back_button.pack(pady=10)
        search_button = tk.Button(content_frame, text="Back to Search", command=ZoekPagina, font=("Helvetica", 16), bg="#FF5722", fg="white", relief="flat", padx=20, pady=10)
        search_button.pack(pady=10)
#Dit maakt de over ons pagina
    def over_ons():
        for widget in content_frame.winfo_children():
            widget.destroy()
        about_label = tk.Label(content_frame, text="About Us", font=("Helvetica", 40, 'bold'), fg='#4CAF50', bg='#F0F0F0')
        about_label.pack(expand=True)
        about_text = tk.Label(content_frame, text="Wij zijn het team Gambling 102 \n(ja er is ook een 101). \nWij hebben in ons team met (op hierarchische volgorde) Jorn, Mika, Cyril, Prosper, Sverre \nhard gewerkt aan deze prachtige applicatie voor de steamopdracht", font=("Helvetica", 20), fg="#333333", bg='#F0F0F0', wraplength=600)
        about_text.pack(pady=200)
    home_button = tk.Button(nav_menu_frame, text="Home", command=Home_Page, font=("Helvetica", 18), bg="#F0F0F0", fg="black", relief="flat")
    home_button.pack(side="left", padx=20, pady=10)
    search_button = tk.Button(nav_menu_frame, text="Search", command=ZoekPagina, font=("Helvetica", 18), bg="#F0F0F0", fg="black", relief="flat")
    search_button.pack(side="left", padx=20, pady=10)
    about_button = tk.Button(nav_menu_frame, text="About Us", command=over_ons, font=("Helvetica", 18), bg="#F0F0F0", fg="black", relief="flat")
    about_button.pack(side="left", padx=20, pady=10)
    genre_btn = tk.Button(nav_menu_frame, text="Genre", command=GenrePagina, font=("Helvetica", 18), bg="#F0F0F0", fg="black", relief="flat")
    genre_btn.pack(side="left", padx=20, pady=10)
    Home_Page()

    DB_SETTINGS = {
        "user": "postgres",
        "password": "wachtwoord",
        "host": "20.229.115.179",
        "port": "5432",
        "database": "steamdatabase"
    }
    #Dit is de code om de datebase te verbinden
    def Database_start():
        try:
            connection = psycopg2.connect(**DB_SETTINGS)
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_logs (
                    id SERIAL PRIMARY KEY,
                    query TEXT NOT NULL,
                    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error setting up the database: {e}")
    def zoek_Handle(log):
        search_query = ''
        if search_query:
            try:
                connection = psycopg2.connect(**DB_SETTINGS)
                cursor = connection.cursor()
                cursor.execute("INSERT INTO search_logs (query) VALUES (%s)", (log,))
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                print(e)
    Database_start()
    knop = False
    while True:
        picodata = serialPort.readline().decode().strip()
        if knop == False:
            #Dit checkt of er beweging is doorgestuurd door de sensor
            if 'BEWEGING' in picodata:
                try:
                    Volgende_pagina()
                    knop = True
                except:
                    print("Je moet nog even een game selecteren")
        if "BEWEGING" not in picodata:
            knop = False
        root.mainloop()
else:
    print("Het is bedtijd jongeman, ga slapen")