import tkinter as tk #pip install tkinter
from tkinter import ttk, messagebox
from collections import Counter
import random

# Kartenwerte & Farben
RANKS = '23456789TJQKA'
SUITS = 'hdcs'
RANK_MAPPING = {r: i + 2 for i, r in enumerate(RANKS)}

# Startkapital
player_chips = 500

# Berechne Wahrscheinlichkeit für bessere Hand
def calculate_probability(strength):
    remaining_cards = 52 - 5  # Deck ohne eigene Karten
    better_hands = max(0, (100 - strength) / 100) * remaining_cards  # Je niedriger die Hand, desto mehr bessere gibt es
    return round((better_hands / remaining_cards) * 100, 2)  # Wahrscheinlichkeit in %

# Pokerhand analysieren mit besserer Logik
def evaluate_hand(cards):
    ranks = sorted([RANK_MAPPING[c[0]] for c in cards], reverse=True)
    suits = [c[1] for c in cards]

    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    is_flush = max(suit_counts.values()) == 5
    is_straight = len(rank_counts) == 5 and max(ranks) - min(ranks) == 4
    max_rank = max(ranks)

    if is_straight and is_flush:
        return 90 + max_rank  # Straight Flush
    elif 4 in rank_counts.values():
        return 80 + max_rank  # Vierling
    elif sorted(rank_counts.values()) == [2, 3]:
        return 70 + max_rank  # Full House
    elif is_flush:
        return 60 + max_rank  # Flush
    elif is_straight:
        return 50 + max_rank  # Straße
    elif 3 in rank_counts.values():
        return 40 + max_rank  # Drilling
    elif list(rank_counts.values()).count(2) == 2:
        return 30 + max_rank  # Zwei Paare
    elif 2 in rank_counts.values():
        return 20 + max_rank  # Ein Paar
    return 10 + max_rank  # Hohe Karte

# Empfehlung für den Einsatz basierend auf Handstärke & Wahrscheinlichkeiten
def get_recommended_action(strength, opponent_bet):
    global player_chips

    if opponent_bet > player_chips:
        return "Zu wenig Chips für diesen Call!"

    probability = calculate_probability(strength)
    pot_odds = opponent_bet / (player_chips + opponent_bet)

    if probability < 10:  
        return "All-In! Starke Hand."
    elif probability < 25:  
        return "Call oder kleiner Raise."
    elif probability < 40:  
        return "Call mit Vorsicht."
    elif probability < 60:  
        return "Check oder kleiner Call."
    return "Fold – hohe Wahrscheinlichkeit einer besseren Hand."

# Berechnung & Anzeige
def calculate():
    global player_chips
    try:
        cards = [(rank_vars[i].get(), suit_vars[i].get()) for i in range(5)]
        strength = evaluate_hand(cards)
        probability = calculate_probability(strength)

        result_label.config(text=f"Handstärke: {strength}\nChance auf bessere Hand: {probability}%")

    except Exception as e:
        result_label.config(text=f"Fehler: {e}")

# Gegnerreaktion
def evaluate_opponent():
    global player_chips
    try:
        opponent_bet = int(opponent_bet_entry.get())
        strength = int(result_label.cget("text").split(":")[1].split("\n")[0])
        recommendation = get_recommended_action(strength, opponent_bet)

        if opponent_bet <= player_chips:
            player_chips -= opponent_bet
            chip_label.config(text=f"Chips: {player_chips}")

        action_label.config(text=f"Empfehlung: {recommendation}")

    except ValueError:
        messagebox.showwarning("Fehler", "Bitte gib eine gültige Zahl für den gegnerischen Einsatz ein!")

# GUI erstellen
root = tk.Tk()
root.title("Poker Bot")
root.geometry("400x650")
root.configure(bg="#1A001A")

style = ttk.Style()
style.configure("TButton", background="#800080", foreground="white", font=("Arial", 12), padding=5)
style.configure("TLabel", background="#1A001A", foreground="white", font=("Arial", 12))

# Chip-Anzeige
chip_label = ttk.Label(root, text=f"Chips: {player_chips}", background="#1A001A", foreground="white", font=("Arial", 14))
chip_label.pack(pady=5)

# Kartenwahl
ttk.Label(root, text="Wähle deine Karten:", background="#1A001A", foreground="white", font=("Arial", 14)).pack(pady=5)

rank_vars = [tk.StringVar(value="A") for _ in range(5)]
suit_vars = [tk.StringVar(value="h") for _ in range(5)]

for i in range(5):
    frame = ttk.Frame(root)
    frame.pack(pady=2)
    ttk.Label(frame, text=f"Karte {i+1}:", background="#1A001A", foreground="white").grid(row=0, column=0, padx=5)
    ttk.Combobox(frame, textvariable=rank_vars[i], values=list(RANK_MAPPING.keys()), width=3).grid(row=0, column=1)
    ttk.Combobox(frame, textvariable=suit_vars[i], values=list(SUITS), width=3).grid(row=0, column=2)

# Button für Berechnung
calc_button = ttk.Button(root, text="Berechne Handstärke", command=calculate)
calc_button.pack(pady=10)

# Ergebnisanzeige
result_label = ttk.Label(root, text="", background="#1A001A", foreground="white", font=("Arial", 12))
result_label.pack(pady=10)

# Gegner-Einsatz Eingabe
ttk.Label(root, text="Gegnerischer Einsatz:", background="#1A001A", foreground="white").pack(pady=5)
opponent_bet_entry = ttk.Entry(root)
opponent_bet_entry.pack(pady=5)

# Button für Gegnerreaktion
evaluate_button = ttk.Button(root, text="Reagiere auf Gegner", command=evaluate_opponent)
evaluate_button.pack(pady=10)

# Ergebnis der Gegneraktion
action_label = ttk.Label(root, text="", background="#1A001A", foreground="white", font=("Arial", 12))
action_label.pack(pady=10)

root.mainloop()
