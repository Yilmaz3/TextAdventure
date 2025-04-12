from module.utils import Inventar, slow_print

class Charakter:
    """Repräsentiert einen Charakter im Gefängnis."""
    gefängnis_name = "Sona Prison"  # Name des Gefängnisses

    def __init__(self, name: str, haftdauer: int):
        # Initialisiert einen Charakter mit Name und Haftdauer
        self._name = name  # Name des Charakters
        self._haftdauer = haftdauer  # Haftdauer in Jahren
        self.inventar = Inventar()  # Inventar des Charakters

    @property
    def name(self) -> str:
        return self._name  # Gibt den Namen des Charakters zurück

    @property
    def haftdauer(self) -> int:
        return self._haftdauer  # Gibt die Haftdauer des Charakters zurück

    @haftdauer.setter
    def haftdauer(self, value: int):
        # Überprüft, ob die Haftdauer nicht negativ ist
        if value < 0:
            raise ValueError("Haftdauer darf nicht negativ sein.")
        self._haftdauer = value  # Setzt die neue Haftdauer

    @staticmethod
    def gefängnis_info() -> str:
        # Gibt allgemeine Informationen über das Gefängnis zurück
        return f"Willkommen in {Charakter.gefängnis_name}. Niemand entkommt hier."

    def beschreibe(self) -> str:
        # Gibt eine Beschreibung des Charakters zurück
        return f"Gefangener: {self.name}, Haftdauer: {self.haftdauer} Jahre."


class Ausbrecher(Charakter):
    """Repräsentiert einen Ausbrecher mit einem speziellen Plan."""
    def __init__(self, name: str, haftdauer: int, ausbruchsplan: str):
        # Initialisiert einen Ausbrecher mit Name, Haftdauer und Ausbruchsplan
        super().__init__(name, haftdauer)
        self.ausbruchsplan = ausbruchsplan  # Ausbruchsplan des Charakters

    def beschreibe(self) -> str:
        # Gibt eine erweiterte Beschreibung des Ausbrechers zurück
        return f"{super().beschreibe()} Ausbruchsplan: {self.ausbruchsplan}."


def erstelle_charaktere(voller_name: str):
    """Erstellt und zeigt die Charaktere im Gefängnis an."""
    # Erzeugt die Hauptcharaktere
    du = Ausbrecher(voller_name, 15, "Tunnel raus bauen")  # Hauptcharakter
    whistler = Ausbrecher("James Whistler", 80, "Zusammenarbeit mit dir")  # Nebencharakter
    tbag = Ausbrecher("Theodore 'T-Bag' Bagwell", 80, "Beobachtet jeden Schritt")  # Nebencharakter

    # Gibt die Charaktere im Gefängnis aus
    ("\nCharaktere im Gefängnis:")
    (du.beschreibe())  # Beschreibung des Hauptcharakters
    (whistler.beschreibe())  # Beschreibung von Whistler
    (tbag.beschreibe())  # Beschreibung von T-Bag

    return du, whistler, tbag  # Gibt die erstellten Charaktere zurück
