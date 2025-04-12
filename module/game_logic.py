from module.charaktere import erstelle_charaktere
from module.räume import erstelle_cafeteria, erstelle_werkstatt, erstelle_tunnel, Außen, WächterKonflikt

class GameLogic:
    def __init__(self, display_callback, input_callback):
        self.display = display_callback
        self.ask_input = input_callback
        self.action_callback = None
        self.image_callback = None

        self.state = "vorname"
        self.spiel_beendet = False
        self.spieler = None
        self.fullname = ""
        self.vorname = ""
        self.nachname = ""

        self.du = None
        self.whistler = None
        self.tbag = None
        self.cafeteria = None
        self.werkstatt = None
        self.tunnel = None
        self.außen = None
        self.current_room = None

        self.labyrinth_index = 0
        self.labyrinth_chancen = 3
        self.labyrinth_lösung = ["rechts", "links", "rechts", "rechts", "links", "links"]
        self.in_wächter_entscheidung = False
        self.tunnel_start_tbag = False
        self.tunnel_start_whistler = False
        self.messer_rettung_erfolgt = False
        self.tunnel_ergebnis = ""

    def set_action_callback(self, callback):
        self.action_callback = callback

    def set_image_callback(self, callback):
        self.image_callback = callback

    def start_game(self):
        if self.image_callback:
            self.image_callback("sona_start.png")
        self.display("Wie lautet dein Vorname?")

    def on_text_input(self, text: str):
        if self.spiel_beendet:
            self.display("Das Spiel ist vorbei. Klicke auf 'Neustart', um neu zu starten.")
            return

        # Überprüfung auf nur Buchstaben und nicht-leere Eingabe
        if self.state == "vorname":
            if not text.isalpha() or len(text.strip()) == 0:
                self.display("Bitte gib einen gültigen Vornamen ein (nur Buchstaben!).")
                return  # Ungültige Eingabe, erneut fragen
            self.vorname = text.strip()
            self.state = "nachname"
            self.display("Wie lautet dein Nachname?")

        elif self.state == "nachname":
            if not text.isalpha() or len(text.strip()) == 0:
                self.display("Bitte gib einen gültigen Nachnamen ein (nur Buchstaben!).")
                return  # Ungültige Eingabe, erneut fragen
            self.nachname = text.strip()
            self.fullname = f"{self.vorname} {self.nachname}"
            self.setup_spiel()

        elif self.state == "labyrinth":
            self.handle_labyrinth_input(text)

        elif self.state == "tunnel_entscheidung":
            if text == "Nach oben gehen":
                self.display("Du gehst nach oben, um die Lage abzuchecken. Plötzlich taucht ein Wächter auf!\nDer Wächter zählt 1 und 1 zusammen und versteht, was hier vor sich geht. Er sperrt dich ein.\nSpiel zu Ende.")
                self.end_game()
            elif text == "Unten bleiben":
                self.display("Du entscheidest dich, unten zu bleiben. Nach einer Weile hörst du Schritte von oben.\nEs scheint, dass ein Wächter direkt vor der Tür war. Zum Glück bist du unten geblieben.\nIhr seid weiterhin sicher und könnt mit dem Plan fortfahren.")
                self.start_außen_sequence()
            return

        elif self.state == "aussen_entscheidung":
            if text == "T-Bag verraten":
                self.display(self.außen.tbag_verraten(self.spieler))
                self.end_game()
            elif text == "T-Bag nicht verraten":
                self.display(self.außen.tbag_nicht_verraten(self.spieler))
                self.state = "labyrinth"
                self.labyrinth_index = 0
                self.labyrinth_chancen = 3
                self.ask_for_labyrinth_direction()
            return

        elif self.in_wächter_entscheidung:
            self.handle_wächter_entscheidung(text)

    def setup_spiel(self):
        self.du, self.whistler, self.tbag = erstelle_charaktere(self.fullname)
        self.spieler = self.du
        self.cafeteria = erstelle_cafeteria()
        self.werkstatt = erstelle_werkstatt()
        self.tunnel = erstelle_tunnel()
        self.current_room = self.cafeteria
        self.state = "ingame"
        self.display(f"""
        Du bist {self.fullname}, Insasse des berüchtigten Sona Prison.
        Dein Ziel ist es, einen Ausbruchsplan zu schmieden und zu entkommen.
        Eine Mafiafamilie hat dich in den Knast geschickt, damit du deren Boss rettest!
        Befreunde dich mit Insassen, da mehr Freunde auch gleich mehr Möglichkeiten bedeutet.
        Aber Vorsicht: Andere Gefangene könnten so tun, als wären sie Freunde, aber dich hintergehen.
        """)

        self.display("\nCharaktere im Gefängnis:")
        self.display(self.du.beschreibe())
        self.display(self.whistler.beschreibe())
        self.display(self.tbag.beschreibe())

        if self.image_callback:
            self.image_callback("cafeteria.png")
        self.display(self.current_room.beschreibung)
        self.show_actions()

    def on_action_selected(self, aktion):
        if self.state == "labyrinth":
            self.handle_labyrinth_input("1" if aktion == "Rechts" else "2")
            return

        if self.state == "tunnel_entscheidung" or self.state == "aussen_entscheidung":
            self.on_text_input(aktion)
            return

        if self.in_wächter_entscheidung:
            self.handle_wächter_entscheidung("1" if aktion == "Verstecken" else "2")
            return

        if self.spiel_beendet or not self.current_room:
            return

        ergebnis = self.current_room.interagiere(aktion, self.spieler)
        self.display(ergebnis)

        if self.current_room.name == "Cafeteria":
            if aktion == "Mit T-Bag mitgehen":
                self.current_room = self.werkstatt
                if self.image_callback:
                    self.image_callback("werkstatt.png")
                self.display(self.current_room.beschreibung)
            elif aktion == "Mit Whistler mitgehen":
                self.current_room = self.tunnel
                if self.image_callback:
                    self.image_callback("tunnel.png")
                self.display(self.current_room.beschreibung)
                self.action_callback(["Anfangen zu graben"])
                self.tunnel_start_whistler = True
                return
            elif "Spiel zu Ende" in ergebnis:
                self.end_game()
                return

        elif self.current_room.name == "Werkstatt":
            if "Wächter entdeckt" in ergebnis:
                self.in_wächter_entscheidung = True
                if self.image_callback:
                    self.image_callback("wächter.png")
                self.display(WächterKonflikt.interagiere(self.spieler))
                self.action_callback(["Verstecken", "Nicht verstecken"])
                return
            elif "Spiel zu Ende" in ergebnis:
                self.end_game()
                return
            elif aktion == "Zurück zur Cafeteria gehen":
                self.display("Du kehrst in die Cafeteria zurück.")
                self.end_game()
                return

        elif self.current_room.name == "Tunnel":
            if aktion == "Anfangen zu graben":
                self.display("Du beginnst mit dem Graben...")
                self.tunnel_start_whistler = True
            elif aktion == "Helfen weiterzugraben":
                self.tunnel_start_tbag = True

            if self.tunnel_start_whistler or self.tunnel_start_tbag:
                self.tunnel_ergebnis = self.tunnel.interagiere("Weiter graben", self.spieler)
                self.display(self.tunnel_ergebnis)

            if "rettest euch" in self.tunnel_ergebnis:
                self.messer_rettung_erfolgt = True
                if self.image_callback:
                    self.image_callback("tunnel_gerettet.png")
                self.display("Was machst du?")
                self.action_callback(["Nach oben gehen", "Unten bleiben"])
                self.state = "tunnel_entscheidung"
                return

            if "Spiel zu Ende" in self.tunnel_ergebnis and "rettest euch" not in self.tunnel_ergebnis:
                if self.image_callback:
                    self.image_callback("tunnel_einsturz.png")
                self.end_game()
                return
            elif "Decke" in self.tunnel_ergebnis and "rettest euch" not in self.tunnel_ergebnis:
                if self.image_callback:
                    self.image_callback("tunnel_einsturz.png")
                self.end_game()
                return
            elif "Außenwelt" in self.tunnel_ergebnis:
                self.start_außen_sequence()
                return

        elif self.current_room.name == "Außen":
            if "Labyrinth" in ergebnis:
                self.state = "labyrinth"
                self.labyrinth_index = 0
                self.labyrinth_chancen = 3
                self.ask_for_labyrinth_direction()
                return
            elif "Spiel zu Ende" in ergebnis:
                self.end_game()
                return

        if hasattr(self.spieler, "status") and self.spieler.status == "tot":
            self.end_game()
            return

        self.show_actions()

    def handle_wächter_entscheidung(self, text: str):
        self.in_wächter_entscheidung = False
        if text == "1" or text == "Verstecken":
            self.current_room = self.tunnel
            if self.image_callback:
                self.image_callback("tunnel.png")
            self.display(f"""Ihr habt euch Erfolgreich versteckt.
            Der Wächter hat euch nicht entdeckt.
            Aber ihr habt Whistler zurückgelassen. Er ist jetzt alleine.
            Ihr macht euch auf den Weg zum Tunnel...
                         Endlich angekommen!
                         Whistler ist schon weit gekommen. Du hilfst ihm.""")
            self.action_callback(["Helfen weiterzugraben"])
            return
        elif text == "2" or text == "Nicht verstecken":
            self.display(WächterKonflikt.nicht_verstecken(self.spieler))
            self.end_game()
            return

    def show_actions(self):
        if self.current_room and self.action_callback:
            aktionen = list(self.current_room.aktionen.keys())
            if aktionen:
                self.display("Was möchtest du tun?")
                for a in aktionen:
                    self.display(f"- {a}")
            self.action_callback(aktionen)

    def start_außen_sequence(self):
        self.außen = Außen()
        self.current_room = self.außen
        self.display(self.außen.start(self.spieler))
        self.state = "aussen_entscheidung"
        if hasattr(self.spieler, "status") and self.spieler.status == "tot":
            self.end_game()
            return
        self.show_actions()

    def ask_for_labyrinth_direction(self):
        self.display(
            f"Weg {self.labyrinth_index + 1}/{len(self.labyrinth_lösung)} – Wähle:\n1. Rechts\n2. Links"
        )
        if self.action_callback:
            self.action_callback(["Links", "Rechts"])
            if self.image_callback:
                self.image_callback("wald.png")

    def handle_labyrinth_input(self, text: str):
        if text not in ["2", "1"]:
            self.display("Ungültige Eingabe. Wähle 1 oder 2.")
            self.ask_for_labyrinth_direction()
            return

        eingabe = "rechts" if text == "1" else "links"
        korrekt = self.labyrinth_lösung[self.labyrinth_index]

        if eingabe == korrekt:
            self.labyrinth_index += 1
            if self.labyrinth_index == len(self.labyrinth_lösung):
                self.display("✅ Ihr habt das Labyrinth erfolgreich durchquert! Der dichte Wald öffnet sich, und ihr erreicht das Flugfeld.\n"
            "Der Privatjet wartet auf euch, und ihr steigt schnell ein.\n"
            "Gerade noch rechtzeitig hebt der Jet ab, bevor die Polizei euch erreicht.\n"
            "Wie versprochen lässt der Mafiaboss deine Familie laufen...\n"
            "\n30 Jahre später\n"
            "\n🌽 Ihr lebt ein schönes Leben in den Malediven...\n"
            "Du hast dir eine eigene Firma aufgebaut mit deiner Frau und dein Sohn ist ein bekannter Anwalt.\n"
            "\nPlötzlich kommen die Agenten von Whistler wieder... Du musst ihn nochmal befreien...\n"
            "\nAls Drohung zeigen sie dir ein Foto von deinem Sohn, wie er gekidnappt worden ist.\n")
                self.display("Fortsetzung folgt...")
                if self.image_callback:
                    self.image_callback("ende.png")
                self.end_game()
            else:
                self.display("✔ Richtig!")
                self.ask_for_labyrinth_direction()
        else:
            self.labyrinth_chancen -= 1
            self.labyrinth_index = 0
            if self.labyrinth_chancen == 0:
                self.display("❌ Ihr habt euch verirrt. Die Polizei hat euch geschnappt.")
                self.end_game()
            else:
                self.display(f"❗ Falsch! Ihr habt noch {self.labyrinth_chancen} Versuche.")
                self.ask_for_labyrinth_direction()

    def end_game(self):
        self.spiel_beendet = True
        self.display("🎮 Spiel beendet. Klicke auf 'Neustart', um neu zu starten.")
        if self.action_callback:
            self.action_callback([])
