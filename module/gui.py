# module/gui.py
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from module.game_logic import GameLogic  # Importiere die Spiel-Logik

class TextAdventureGUI(ctk.CTk):
    """
    Die Hauptklasse für die GUI des Textadventures, die die Anzeige des Spiels übernimmt
    und mit der Logik des Spiels interagiert.
    """
    def __init__(self):
        """
        Initialisiert die GUI und richtet alle wichtigen Komponenten ein,
        einschließlich der Frames, der Texteingabe und der Buttons.
        """
        super().__init__()
        self.title("Gefängnis Textadventure")
        self.geometry("1200x700")

        # Store the initial window size - is needed for font size calculation
        self.previous_width = self.winfo_width()
        self.previous_height = self.winfo_height()

        # Initialisiert die Spiel-Logik und setzt Callbacks für Aktionen und Bilder
        self.logic = GameLogic(self.display_output, self.get_player_input)
        self.logic.set_action_callback(self.display_actions)
        self.logic.set_image_callback(self.update_image)

        # Layout: Links = Text + Buttons / Rechts = Bild
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        self.left_frame = ctk.CTkFrame(main_frame, width=700)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ctk.CTkFrame(main_frame, width=1000)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # === Bildbereich ===
        self.image_label = ctk.CTkLabel(self.right_frame, text="")
        self.image_label.pack(expand=True)
        self.tk_image = None
        self.update_image("sona_start.png")  # Anfangsbild

        # === Textfeld ===
        self.output_box = ctk.CTkTextbox(self.left_frame, width=980, height=550, wrap="word")
        self.output_box.pack(pady=10)
        self.output_box.configure(state="disabled")

        # === Eingabezeile + Button ===
        input_frame = ctk.CTkFrame(self.left_frame)
        input_frame.pack(pady=5)

        self.input_entry = ctk.CTkEntry(input_frame, width=780)
        self.input_entry.pack(side="left", padx=5)
        self.input_entry.bind("<Return>", lambda event: self.on_input_submit())

        self.send_button = ctk.CTkButton(input_frame, text="Senden", command=self.on_input_submit)
        self.send_button.pack(side="left")

        # === Aktionsbuttons ===
        self.button_frame = ctk.CTkFrame(self.left_frame)
        self.button_frame.pack(pady=10)

        # === Inventar + Neustart ===
        utility_frame = ctk.CTkFrame(self.left_frame)
        utility_frame.pack(pady=10)

        self.inventar_button = ctk.CTkButton(utility_frame, text="Inventar anzeigen", command=self.show_inventory)
        self.inventar_button.pack(side="left", padx=10)

        self.restart_button = ctk.CTkButton(utility_frame, text="Neustart", command=self.restart_game)
        self.restart_button.pack(side="left", padx=10)

        # Initialer Text an den Spieler
        self.display_output("Hey Spieler! Schön dich zu sehen! Naja.... der Ort ist jetzt nicht so passend... Aber... Wie heißt du überhaupt?")
        self.logic.start_game()

        # Binde die Fenstergrößenänderung an eine Methode
        self.bind("<Configure>", self.update_font_size)

    def update_image(self, filename):
        """
        Aktualisiert das angezeigte Bild im rechten Bereich der GUI.

        :param filename: Der Name der Bilddatei, die angezeigt werden soll
        """
        try:
            base_path = "./" # os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_path, "images", filename)
            image = Image.open(image_path).resize((600, 700))
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.tk_image)
        except Exception as e:
            self.image_label.configure(text="(Bild konnte nicht geladen werden)")
            print(f"Bildfehler: {e}")

    def update_font_size(self, event):
        """
        Aktualisiert die Schriftgröße im Textbereich, wenn das Fenster geändert wird.

        :param event: Das Event der Fensteränderung
        """
        new_width = self.winfo_width()
        new_height = self.winfo_height()

        # Überprüfen, ob die Fenstergröße geändert wurde
        if new_width != self.previous_width or new_height != self.previous_height:
            # Berechnet die neue Schriftgröße basierend auf der Fensterbreite
            min_font_size = 9
            max_font_size = 30
            new_font_size = max(min(event.width // 100, max_font_size), min_font_size)  # Beispiel: Schriftgröße basierend auf der Breite
            self.output_box.configure(font=("Abdos", new_font_size))

            # Aktualisiere die gespeicherte Fenstergröße
            self.previous_width = new_width
            self.previous_height = new_height

    def display_output(self, text: str):
        """
        Zeigt den Text langsam an, um ein "Tippen" im Textbereich zu simulieren.

        :param text: Der anzuzeigende Text
        """
        if not hasattr(self, "output_queue"):
            self.output_queue = []
            self.printing = False

        self.output_queue.append(text)
        if not self.printing:
            self._start_next_output()

    def _start_next_output(self):
        """
        Startet das Anzeigen des nächsten Texts in der Queue.
        """
        if self.output_queue:
            self.printing = True
            self.output_text = self.output_queue.pop(0)
            self.char_index = 0
            self._print_next_char()
        else:
            self.printing = False

    def _print_next_char(self):
        """
        Zeigt das nächste Zeichen des Textes an.
        """
        if self.char_index < len(self.output_text):
            next_char = self.output_text[self.char_index]
            self.output_box.configure(state="normal") 
            self.output_box.insert("end", next_char)
            self.output_box.see("end")
            self.output_box.configure(state="disabled")
            self.char_index += 1
            self.after(5, self._print_next_char)  # Geschwindigkeit hier einstellbar
        else:
            self.output_box.configure(state="normal")
            self.output_box.insert("end", "\n\n")
            self.output_box.see("end")
            self.output_box.configure(state="disabled")
            self.after(100, self._start_next_output)

    def clear_buttons(self):
        """
        Löscht alle Action-Buttons aus dem Button-Frame.
        """
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def display_actions(self, actions: list[str]):
        """
        Zeigt die verfügbaren Aktionen als Buttons an.

        :param actions: Eine Liste der Aktionen, die der Spieler ausführen kann
        """
        self.clear_buttons()
        for action in actions:
            button = ctk.CTkButton(self.button_frame, text=action,
                                   command=lambda a=action: self.logic.on_action_selected(a))
            button.pack(side="left", padx=5)

    def on_input_submit(self):
        """
        Wird aufgerufen, wenn der Spieler eine Eingabe absendet.
        Verarbeitet die Eingabe und versteckt das Eingabefeld nach der ersten Eingabe.
        """
        eingabe = self.input_entry.get()
        self.input_entry.delete(0, "end")
        self.logic.on_text_input(eingabe)
        if self.logic.nachname != "":
            self.input_entry.pack_forget()  # Eingabefeld ausblenden
            self.send_button.pack_forget()  # Senden-Button ausblenden

    def get_player_input(self, prompt: str):
        """
        Fordert den Spieler zur Eingabe auf, indem ein Prompt angezeigt wird.

        :param prompt: Der Text, der den Spieler zur Eingabe auffordert
        """
        self.display_output(prompt)

    def show_inventory(self):
        """
        Zeigt das Inventar des Spielers an, falls vorhanden.
        """
        if self.logic.spieler:
            gegenstaende = self.logic.spieler.inventar.gegenstände
            if gegenstaende:
                self.display_output("Inventar: " + ", ".join(gegenstaende))
            else:
                self.display_output("Dein Inventar ist leer.")

    def restart_game(self):
        """
        Setzt das Spiel zurück und startet es erneut.
        """
        self.output_box.delete("1.0", "end")
        self.logic = GameLogic(self.display_output, self.get_player_input)
        self.logic.set_action_callback(self.display_actions)
        self.logic.set_image_callback(self.update_image)
        self.input_entry.pack(side="left", padx=5)
        self.send_button.pack(side="left")
    
        self.display_output("Hey Spieler! Schön dich zu sehen! Naja.... der Ort ist jetzt nicht so passend... Aber... Wie heißt du überhaupt?")
        self.logic.start_game()
