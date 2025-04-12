class Aktionen:
    def __init__(self, name: str, beschreibung: str, aktionen: dict[str, callable]):
        self.name = name
        self.beschreibung = beschreibung
        self.aktionen = aktionen

    def interagiere(self, aktion: str, spieler) -> str:
        if aktion in self.aktionen:
            return self.aktionen[aktion](spieler)
        return ""


class Cafeteria(Aktionen):
    def __init__(self):
        super().__init__(
            name="Cafeteria",
            beschreibung="Hier treffen sich die Gefangenen, um zu essen, Pläne zu schmieden oder Streitigkeiten zu klären.",
            aktionen={
                "Mit Whistler reden": self.mit_whistler_reden,
                "Ein Messer stehlen": self.ein_messer_stehlen,
                "Einfach essen": self.einfach_essen,
            },
        )

    def mit_whistler_reden(self, spieler) -> str:
        self.aktionen = {
            "Weiter mit Whistler reden": self.weiter_mit_whistler_reden,
            "Unauffällig von Whistler weggehen": self.unauffällig_weggehen,
        }
        return (
            "Whistler: Na Sportsfreund, wie läuft dein Plan? Du bist ja berühmt für deine Ausbrüche. Was schlägst du vor?\n"
            "Stille... Du denkst nach...\n"
            "Während du nachdenkst, bemerkst du, dass T-Bag, dein alter Zellenkompane, euch belauscht hat.\n"
            "Was machst du jetzt?"
        )

    def ein_messer_stehlen(self, spieler) -> str:
        spieler.inventar.hinzufügen("Messer")
        self.aktionen = {
            "Mit Whistler reden": self.mit_whistler_reden,
            "Einfach essen": self.einfach_essen,
        }
        return "Du hast ein Messer gestohlen. Das könnte sehr wichtig werden. Was machst du jetzt?"

    def einfach_essen(self, spieler) -> str:
        return (
            "Jemand stolpert über deine Weste, die plötzlich auf dem Boden liegt.\n"
            "Er wird wütend und ersticht dich.\nSpiel zu Ende."
        )

    def weiter_mit_whistler_reden(self, spieler) -> str:
        self.aktionen = {
            "Mit T-Bag mitgehen": self.mit_tbag_mitgehen,
            "Mit Whistler mitgehen": self.mit_whistler_mitgehen,
        }
        return (
            "Du erklärst Whistler deinen Plan: Nachts langsam und vorsichtig einen Tunnel zum Ausgang graben.\n"
            "Ihr braucht eine Schaufel. Plötzlich taucht T-Bag auf – er hat alles mitgehört...\n"
            "Er sagt, er weiß, wo man eine Schaufel bekommt. Ihr habt keine Wahl. Wohin gehst du?"
        )

    def unauffällig_weggehen(self, spieler) -> str:
        return (
            "Du versuchst unauffällig von Whistler wegzugehen und in deine Zelle zu gelangen.\n"
            "Doch auf dem Weg kommt T-Bag von hinten, schnappt sich eine Pfanne und schlägt sie dir auf den Kopf.\n"
            "Du bist tot.\nSpiel zu Ende."
        )

    def mit_tbag_mitgehen(self, spieler) -> str:
        return (
            "Du folgst T-Bag in eine dunkle Ecke der Cafeteria. Er zeigt dir, wo die Schaufel versteckt ist.\n"
            "Er sagt, dass du ihn dieses Mal lieber nicht verraten sollst wie beim letzten Mal...\n"
            "Sonst würde er dieses Mal schlimmer handeln.\n"
            "Ihr geht gemeinsam in die Werkstatt – dort liegt die Schaufel versteckt.\n"
            "Aber du musst sie selbst klauen... oder zurück in die Cafeteria gehen."
        )

    def mit_whistler_mitgehen(self, spieler) -> str:
        if "Schaufel" not in spieler.inventar.gegenstände:
            spieler.inventar.hinzufügen("Schaufel")
        return (
            "Du entscheidest dich, Whistler zu folgen. Zusammen geht ihr zum Ort, wo der Tunnel gemacht werden soll.\n"
            "Nach einer kurzen Beobachtung kommt auch T-Bag mit der Schaufel.\n"
            "Die Freiheit ist greifbar nahe."
        )


class Werkstatt(Aktionen):
    def __init__(self):
        super().__init__(
            name="Werkstatt",
            beschreibung=(
                "Ein Ort, an dem Sachen hergestellt oder gestohlen werden können.\n"
                "Ein gefährlicher Ort für Neuankömmlinge, aber hier kann man wertvolle Gegenstände finden."
            ),
            aktionen={
                "Schaufel klauen": self.schaufel_klauen,
                "Zurück zur Cafeteria gehen": self.zurueck_zur_cafeteria,
            },
        )

    def schaufel_klauen(self, spieler) -> str:
        if "Schaufel" in spieler.inventar.gegenstände:
            return "Du hast die Schaufel bereits. Es gibt hier nichts mehr zu tun."
        spieler.inventar.hinzufügen("Schaufel")
        return "Wächter entdeckt dich mit der Schaufel!"  # Signal für game_logic.py

    def zurueck_zur_cafeteria(self, spieler) -> str:
        return (
            "Du kehrst in die Cafeteria zurück, doch die Last wird zu viel...\n"
            "Du verlierst den Verstand und nimmst dir das Leben.\n"
            "Spiel zu Ende."
        )


class Tunnel(Aktionen):
    def __init__(self):
        super().__init__(
            name="Tunnel",
            beschreibung="Hier beginnt euer Tunnelbau. Die Freiheit ist greifbar nahe.",
            aktionen={
                "Weiter graben": self.weiter_graben,
            },
        )

    def weiter_graben(self, spieler) -> str:
        if "Schaufel" not in spieler.inventar.gegenstände:
            return "Ihr habt keine Schaufel! Holt sie aus der Werkstatt!"

        if "Messer" not in spieler.inventar.gegenstände:
            spieler.status = "tot"
            return (
                "Ihr beginnt mit dem Graben...\n"
                "Doch plötzlich stürzt ein Teil der Decke ein!\n"
                "Du hattest kein Messer, um sie zu stützen.\n"
                "Du wirst lebendig begraben.\n"
                "Spiel zu Ende."
            )

        return (
            "Du rettest euch mit dem Messer!\n"
            "Der Tunnel drohte einzustürzen, aber du hast geistesgegenwärtig das Messer in die Decke gerammt.\n"
            "So konnte der Einsturz verhindert werden. Ihr habt Glück gehabt!\n"
            "Doch es bleibt keine Zeit zu feiern – bald kommen die Wächter...\n"
            "T-Bag schlägt vor, dass du nach oben gehst und die Lage abcheckst.\n"
            "Was machst du?"
        )


class Außen(Aktionen):
    def __init__(self):
        super().__init__(
            name="Außen",
            beschreibung="Der letzte Schritt zur Freiheit – aber jede Entscheidung zählt.",
            aktionen={
                "T-Bag verraten": self.tbag_verraten,
                "T-Bag nicht verraten": self.tbag_nicht_verraten,
            },
        )
        self.labyrinth_lösungen = ["rechts", "links", "rechts", "rechts", "links", "links"]
        self.max_chancen = 3

    def start(self, spieler) -> str:
        return (
            "Vom Schlitz des Tunnels siehst du die Wächter, wie sie perfekt positioniert sind, damit ihr abhauen könnt.\n"
            "Aufeinmal will T-Bag unüberlegt rauslaufen und vernichtet damit fast den ganzen Plan\n"
            "Du platzst vor Wut und schreist T-Bag an:\n"
            "Wie kann man so dumm und ungeduldig sein?! Wenn du rausläufst, bist du tot und wir alle mit dir!\n"
            "Ab jetzt hörst du nur noch auf mich, oder du bleibst hier unten und verrottest!\n"
            "\nT-Bag bleibt erschrocken stehen und nickt. Ihr wartet gemeinsam weiter auf den perfekten Moment."
            "\nJetzt bleibt nur noch die Entscheidung für den letzten Schritt. Die Freiheit ist greifbar nahe..."
            "Du beginnst den Plan, aber plötzlich überlegst du, ob du T-Bag verraten willst, wie beim letzten Mal...\n"
            "Was machst du?"
        )

    def tbag_verraten(self, spieler) -> str:
        return (
            "Du hast T-Bag verraten! Er rennt aus dem Tunnel und zu den Wächtern.\n"
            "T-Bag zeigt auf den Tunnel und verrät euren Plan.\n"
            "Kurz darauf kommt ein Helikopter und die Wächter schnappen euch.\n"
            "Spiel zu Ende."
        )

    def tbag_nicht_verraten(self, spieler) -> str:
        return (
            "Du entscheidest dich, T-Bag nicht zu verraten.\n"
            "Zusammen rennt ihr aus dem Tunnel und in die Wälder.\n"
            "Die Wächter bemerken es zu spät, und ihr seid auf der Flucht!\n"
            "Ihr habt es geschafft, fürs Erste sicher zu entkommen. Whistler sagt, dass ein Privatjet auf euch wartet.\n"
            "Doch ihr müsst durch ein Labyrinth im dichten Wald navigieren, um das Flugfeld zu erreichen.\n"
            "Ihr habt nur drei Chancen, das Labyrinth zu bestehen, bevor die Polizei euch einholt!\n"
        )


class WächterKonflikt:
    @staticmethod
    def interagiere(spieler) -> str:
        return (
            "Auf dem Weg zurück entdeckt dich ein Wächter mit der gestohlenen Schaufel!\n"
            "Was möchtest du tun?\n"
            "1. Verstecken\n"
            "2. Nicht verstecken\n"
        )

    @staticmethod
    def verstecken(spieler) -> str:
        tunnel = Tunnel()
        return (
            "Du schaffst es, dich rechtzeitig zu verstecken. Der Wächter denkt, dass er sich versehen hat.\n"
            + tunnel.interagiere("Weiter graben", spieler)
        )

    @staticmethod
    def nicht_verstecken(spieler) -> str:
        return (
            "Der Wächter erwischt dich mit der Schaufel. Du wirst in Einzelhaft gesteckt.\n"
            "Dein Plan ist gescheitert.\nSpiel zu Ende."
        )


def erstelle_cafeteria() -> Cafeteria:
    return Cafeteria()

def erstelle_werkstatt() -> Werkstatt:
    return Werkstatt()

def erstelle_tunnel() -> Tunnel:
    return Tunnel()