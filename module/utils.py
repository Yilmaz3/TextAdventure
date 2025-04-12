import sys
import time

def slow_print(text: str, delay: float = 0.0025):
    """Druckt den Text Buchstabe für Buchstabe mit einer Verzögerung."""
    for char in text:
        sys.stdout.write(char)  # Schreibt jeden Buchstaben einzeln
        sys.stdout.flush()  # Erzwingt das sofortige Schreiben
        time.sleep(delay)  # Verzögerung zwischen den Buchstaben
    print()  # Zeilenumbruch nach dem gesamten Text

class Inventar:
    """Repräsentiert das Inventar eines Charakters."""
    def __init__(self):
        self.gegenstände = []  # Liste für die Gegenstände im Inventar

    def hinzufügen(self, gegenstand: str):
        """Fügt einen Gegenstand dem Inventar hinzu."""
        self.gegenstände.append(gegenstand)  # Gegenstand zur Liste hinzufügen
        print(f"{gegenstand} wurde deinem Inventar hinzugefügt.")  # Bestätigung ausgeben

    def anzeigen(self):
        """Zeigt alle Gegenstände im Inventar an."""
        if not self.gegenstände:
            # Nachricht ausgeben, wenn das Inventar leer ist
            print("Dein Inventar ist leer.")
        else:
            # Liste der Gegenstände ausgeben
            print("Dein Inventar enthält:")
            for item in self.gegenstände:
                print(f"- {item}")  # Einzelne Gegenstände auflisten

