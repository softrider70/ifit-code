#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""iFit Code - Antwortcode fuer den Privileged Mode auf iFit-/NordicTrack-Konsolen.

In Pythonista auf dem iPhone/iPad gestartet, zeigt das Skript eine
Bedienoberflaeche. Im Terminal fragt es nach der Zahl.

    python3 ifit_code.py 123456      # gibt 382410 aus
    python3 ifit_code.py             # fragt nach der Zahl
"""

import sys

MUL = 0x5DEECE66D
ADD = 0xB
MASKE = (1 << 48) - 1
OBERGRENZE = 999999


def naechste_int(zahl, obergrenze=OBERGRENZE):
    """java.util.Random(seed).nextInt(obergrenze) nachbauen."""
    zustand = (int(zahl) ^ MUL) & MASKE
    while True:
        zustand = (zustand * MUL + ADD) & MASKE
        bits = zustand >> 17  # next(31)
        wert = bits % obergrenze
        # Java verwirft Werte, die den Bereich ungleich verteilen wuerden.
        if bits - wert + (obergrenze - 1) < (1 << 31):
            return wert


def nur_ziffern(text):
    return "".join(c for c in str(text) if c.isdigit())


def antwort(zahl):
    """Sechsstellige Antwort zur angezeigten Zahl."""
    return "%06d" % naechste_int(zahl)


def _ist_pythonista():
    try:
        import ui  # noqa: F401
    except ImportError:
        return False
    return "pythonista" in sys.executable.lower() or sys.platform == "ios"


HELL = {
    "hintergrund": "#f2f2f7",
    "feld": "#ffffff",
    "feld_rahmen": "#d1d1d6",
    "text": "#1c1c1e",
    "neben": "#5f6470",
    "leer": "#8a95a3",
    "akzent": "#0a6ea8",
    "akzent_text": "#ffffff",
    "ok": "#0e7a3c",
}

DUNKEL = {
    "hintergrund": "#0b0f14",
    "feld": "#1c242e",
    "feld_rahmen": "#33404e",
    "text": "#e8eef5",
    "neben": "#93a2b3",
    "leer": "#66748a",
    "akzent": "#4cc2ff",
    "akzent_text": "#04121b",
    "ok": "#37d67a",
}


def _system_ist_hell():
    """Erscheinungsbild des Geraets erfragen; dunkel ist der Rueckfall."""
    try:
        from objc_util import ObjCClass
    except ImportError:
        return False
    try:
        app = ObjCClass("UIApplication").sharedApplication()
        fenster = app.keyWindow()
        if fenster is None:
            fenster = app.windows().objectAtIndex_(0)
        return fenster.traitCollection().userInterfaceStyle() == 1
    except Exception:
        return False


def bedienoberflaeche():
    import clipboard
    import ui

    farbe = HELL if _system_ist_hell() else DUNKEL

    rand = 18
    # Kurze Bildschirmkante = Breite im Hochformat, auch bei Querlage.
    schirm = ui.get_screen_size()
    breite = min(schirm[0], schirm[1])

    # Senkrechte Masse: (Hoehe, Abstand danach)
    masse = (
        (18, 14),
        (68, 16),
        (62, 18),
        (50, 14),
        (44, 0),
    )
    hoehe = rand + sum(h + a for h, a in masse) + rand

    view = ui.View(background_color=farbe["hintergrund"])
    view.name = "iFit Code"
    view.frame = (0, 0, breite, hoehe)
    view.corner_radius = 14

    titel = ui.Label(
        text="IFIT CODE",
        alignment=ui.ALIGN_CENTER,
        text_color=farbe["neben"],
        font=("Menlo-Bold", 13),
    )

    feld = ui.TextField(background_color=farbe["feld"])
    feld.text = ""
    feld.placeholder = "sechsstellige Zahl"
    feld.keyboard_type = ui.KEYBOARD_NUMBER_PAD
    feld.alignment = ui.ALIGN_CENTER
    feld.font = ("Menlo", 32)
    feld.text_color = farbe["text"]
    feld.tint_color = farbe["akzent"]
    feld.border_width = 1
    feld.border_color = farbe["feld_rahmen"]
    feld.corner_radius = 12
    feld.clear_button_mode = "while_editing"

    ergebnis = ui.Label(
        text="------",
        alignment=ui.ALIGN_CENTER,
        text_color=farbe["leer"],
        font=("Menlo-Bold", 40),
    )

    knopf = ui.Button(
        title="Kopieren",
        background_color=farbe["feld"],
        tint_color=farbe["leer"],
        corner_radius=12,
    )
    knopf.font = ("Menlo-Bold", 15)
    knopf.enabled = False

    hinweis = ui.Label(
        text="Die sechsstellige Zahl aus dem Fenster auf der Konsole",
        alignment=ui.ALIGN_CENTER,
        number_of_lines=2,
        text_color=farbe["neben"],
        font=("Menlo", 13),
    )

    stand = {"code": ""}

    def knopf_an(an):
        knopf.enabled = an
        knopf.background_color = farbe["akzent"] if an else farbe["feld"]
        knopf.tint_color = farbe["akzent_text"] if an else farbe["leer"]

    def rechnen(sender=None):
        ziffern = nur_ziffern(feld.text or "")[:6]
        if ziffern != (feld.text or ""):
            feld.text = ziffern

        if not ziffern:
            stand["code"] = ""
            ergebnis.text = "------"
            ergebnis.text_color = farbe["leer"]
            knopf_an(False)
            knopf.title = "Kopieren"
            hinweis.text = "Die sechsstellige Zahl aus dem Fenster auf der Konsole"
            return

        stand["code"] = antwort(ziffern)
        ergebnis.text = stand["code"]
        ergebnis.text_color = farbe["ok"]
        knopf_an(True)
        knopf.title = "Kopieren"
        hinweis.text = (
            "Zahl %s erkannt" % ziffern
            if len(ziffern) == 6
            else "Bisher %d von 6 Ziffern - rechnet schon mit" % len(ziffern)
        )

    def kopieren(sender=None):
        if not stand["code"]:
            return
        clipboard.set(stand["code"])
        knopf.title = "Kopiert"

        def zuruecksetzen():
            knopf.title = "Kopieren"

        ui.delay(zuruecksetzen, 1.2)

    class FeldDelegat(object):
        def textfield_did_change(self, textfield):
            rechnen()

    delegat = FeldDelegat()
    feld.delegate = delegat
    feld.action = rechnen
    knopf.action = kopieren

    view.add_subview(titel)
    view.add_subview(feld)
    view.add_subview(ergebnis)
    view.add_subview(knopf)
    view.add_subview(hinweis)

    elemente = (titel, feld, ergebnis, knopf, hinweis)

    def layout():
        breite_innen = view.width - 2 * rand
        y = rand
        for element, (h, abstand) in zip(elemente, masse):
            element.frame = (rand, y, breite_innen, h)
            y += h + abstand

    view.layout = layout
    layout()
    view.present("sheet")


def terminal():
    print("iFit Code - Antwortcode fuer den Privileged Mode")
    print("Sechsstellige Zahl von der Konsole eingeben, Enter rechnet.")
    print("Leere Eingabe beendet.\n")
    while True:
        try:
            roh = input("Zahl: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not roh:
            break
        ziffern = nur_ziffern(roh)
        if not ziffern:
            print("Keine Ziffer erkannt - bitte die sechsstellige Zahl eingeben.\n")
            continue
        print("Antwort: %s\n" % antwort(ziffern))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ziffern = nur_ziffern(sys.argv[1])
        if not ziffern:
            sys.exit("Keine Ziffern in der Eingabe.")
        print(antwort(ziffern))
    elif _ist_pythonista():
        bedienoberflaeche()
    else:
        terminal()
