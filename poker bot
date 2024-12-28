import tkinter as tk
from tkinter import messagebox
from collections import Counter

class PokerBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Bot")

        # Vollbildmodus
        self.root.attributes('-fullscreen', True)
        
        # Hintergrundfarbe für das Fenster (Schwarz)
        self.root.config(bg="black")
        
        # Hauptrahmen für das Layout
        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Linker Frame für die Ergebnisse (unten)
        self.left_frame = tk.Frame(self.main_frame, bg="black")
        self.left_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Rechter Frame für die Kartenauswahl (oben)
        self.right_frame = tk.Frame(self.main_frame, bg="black")
        self.right_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Karten Eingabe (Label und Eingabefeld)
        self.label = tk.Label(self.left_frame, text="Wähle deine Karten (z. B. Ass Herz):", fg="white", bg="black", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.left_frame, font=("Helvetica", 14), bg="#7a4b96", fg="black")
        self.entry.pack(pady=10)

        self.submit_button = tk.Button(self.left_frame, text="Analyse starten", command=self.analyze_hand, bg="#7a4b96", fg="black", font=("Helvetica", 14))
        self.submit_button.pack(pady=20)

        # Ergebnisbereich
        self.result_label = tk.Label(self.left_frame, text="Ergebnis:", fg="white", bg="black", font=("Helvetica", 14))
        self.result_label.pack()

        self.result_text = tk.Text(self.left_frame, height=15, width=50, bg="#7a4b96", fg="black", font=("Helvetica", 12))
        self.result_text.pack()

        # Karten als Buttons auf der rechten Seite anzeigen
        self.cards = self.create_deck()
        self.card_buttons = []
        for card in self.cards:
            button = tk.Button(self.right_frame, text=card, command=lambda card=card: self.select_card(card), bg="#7a4b96", fg="black", font=("Helvetica", 10), height=1, width=10)
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.card_buttons.append(button)

    def create_deck(self):
        """Erstellt ein Standarddeck mit Karten und deren vollständigen Namen"""
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # Ass wurde hier hinzugefügt
        suits = ['Herz', 'Karo', 'Kreuz', 'Pik']
        deck = [f"{rank} {suit}" for rank in ranks for suit in suits]
        return deck

    def select_card(self, card):
        """Fügt eine ausgewählte Karte in das Eingabefeld ein"""
        current_text = self.entry.get()
        if current_text:
            self.entry.insert(tk.END, " " + card)
        else:
            self.entry.insert(tk.END, card)

    def analyze_hand(self):
        hand_input = self.entry.get()
        cards = hand_input.split()

        if len(cards) != 2:
            messagebox.showerror("Fehler", "Bitte genau zwei Karten eingeben!")
            return

        try:
            result, strategy, decision = self.evaluate_hand(cards)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result + "\n\n" + strategy + "\n\n" + decision)
        except ValueError as e:
            messagebox.showerror("Fehler", str(e))

    def evaluate_hand(self, cards):
        # Poker-Ranking-Berechnung: Vereinfachte Analyse
        ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        suits = ['Herz', 'Karo', 'Kreuz', 'Pik']

        parsed_cards = []
        for card in cards:
            rank, suit = card.split()
            if rank not in ranks or suit not in suits:
                raise ValueError(f"Ungültige Karte: {card}")
            parsed_cards.append((ranks[rank], suit))

        ranks_only = [card[0] for card in parsed_cards]
        suits_only = [card[1] for card in parsed_cards]

        # Evaluierung der Hand (z. B. Paar, gleiche Farbe, etc.)
        result = self.detect_hand(parsed_cards, ranks_only, suits_only)

        # Strategie basierend auf der Hand
        strategy = self.develop_strategy(result)

        # Entscheidung basierend auf der Strategie
        decision = self.make_decision(result)

        return f"Karten: {cards}\n{result}", strategy, decision

    def detect_hand(self, parsed_cards, ranks_only, suits_only):
        result = []
        rank_counts = Counter(ranks_only)
        is_flush = len(set(suits_only)) == 1
        sorted_ranks = sorted(ranks_only)
        is_straight = all(sorted_ranks[i] + 1 == sorted_ranks[i + 1] for i in range(len(sorted_ranks) - 1))

        # Bewertung von speziellen Händen
        if is_flush and sorted_ranks == [10, 11, 12, 13, 14]:
            result.append("Royal Flush")
        elif is_flush and is_straight:
            result.append("Straight Flush")
        elif 4 in rank_counts.values():
            result.append("Four of a Kind")
        elif 3 in rank_counts.values() and 2 in rank_counts.values():
            result.append("Full House")
        elif is_flush:
            result.append("Flush")
        elif is_straight:
            result.append("Straight")
        elif 3 in rank_counts.values():
            result.append("Three of a Kind")
        elif list(rank_counts.values()).count(2) == 2:
            result.append("Two Pair")
        elif 2 in rank_counts.values():
            result.append("One Pair")
        else:
            result.append("High Card")

        return " und ".join(result)

    def develop_strategy(self, hand_type):
        # Erweiterte Strategie für spezifische Handtypen
        if "Royal Flush" in hand_type or "Straight Flush" in hand_type:
            return "Strategie: Gehe All-In, da dies die stärksten Hände im Poker sind."
        elif "Four of a Kind" in hand_type or "Full House" in hand_type:
            return "Strategie: Erhöhe den Einsatz stark, da dies extrem starke Hände sind."
        elif "Flush" in hand_type or "Straight" in hand_type:
            return "Strategie: Spiele aggressiv, da diese Hände stark sind."
        elif "Three of a Kind" in hand_type or "Two Pair" in hand_type:
            return "Strategie: Spiele vorsichtig, aber setze, um Druck auszuüben."
        elif "One Pair" in hand_type:
            return "Strategie: Ziehe Mitgehen oder einen kleinen Einsatz in Betracht."
        else:
            return "Strategie: Überlege zu passen, da die Hand schwach ist."

    def make_decision(self, hand_type):
        # Erweiterte Entscheidungslogik basierend auf Handtyp
        if "Royal Flush" in hand_type or "Straight Flush" in hand_type:
            return "Entscheidung: All-In"
        elif "Four of a Kind" in hand_type or "Full House" in hand_type:
            return "Entscheidung: Raise (Erhöhen)"
        elif "Flush" in hand_type or "Straight" in hand_type:
            return "Entscheidung: Raise"
        elif "Three of a Kind" in hand_type or "Two Pair" in hand_type:
            return "Entscheidung: Call (Mitgehen)"
        elif "One Pair" in hand_type:
            return "Entscheidung: Check (Abwarten)"
        else:
            return "Entscheidung: Fold (Passen)"

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerBot(root)
    root.mainloop()
