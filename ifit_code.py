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


def bedienoberflaeche():
    import clipboard
    import ui

    rand = 16

    view = ui.View(background_color="#0b0f14")
    view.name = "iFit Code"
    view.frame = (0, 0, 320, 300)

    titel = ui.Label(
        text="IFIT CODE",
        alignment=ui.ALIGN_CENTER,
        text_color="#8394a6",
        font=("Menlo-Bold", 13),
    )

    feld = ui.TextField(background_color="#151b23")
    feld.placeholder = "sechsstellige Zahl"
    feld.keyboard_type = ui.KEYBOARD_NUMBER_PAD
    feld.alignment = ui.ALIGN_CENTER
    feld.font = ("Menlo", 32)
    feld.text_color = "#e8eef5"
    feld.tint_color = "#4cc2ff"
    feld.border_width = 1
    feld.border_color = "#26303b"
    feld.corner_radius = 12
    feld.clear_button_mode = "while_editing"

    ergebnis = ui.Label(
        text="------",
        alignment=ui.ALIGN_CENTER,
        text_color="#4a5866",
        font=("Menlo-Bold", 40),
    )

    knopf = ui.Button(
        title="Kopieren",
        background_color="#1c242e",
        tint_color="#4cc2ff",
        corner_radius=12,
    )
    knopf.font = ("Menlo-Bold", 15)
    knopf.enabled = False

    hinweis = ui.Label(
        text="Die sechsstellige Zahl aus dem Fenster auf der Konsole",
        alignment=ui.ALIGN_CENTER,
        number_of_lines=2,
        text_color="#8394a6",
        font=("Menlo", 11),
    )

    stand = {"code": ""}

    def rechnen(sender=None):
        ziffern = nur_ziffern(feld.text)[:6]
        if ziffern != feld.text:
            feld.text = ziffern

        if not ziffern:
            stand["code"] = ""
            ergebnis.text = "------"
            ergebnis.text_color = "#4a5866"
            knopf.enabled = False
            knopf.title = "Kopieren"
            hinweis.text = "Die sechsstellige Zahl aus dem Fenster auf der Konsole"
            return

        stand["code"] = antwort(ziffern)
        ergebnis.text = stand["code"]
        ergebnis.text_color = "#e8eef5"
        knopf.enabled = True
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

    def layout():
        breite = view.width - 2 * rand
        y = 16
        titel.frame = (rand, y, breite, 20)
        y += 32
        feld.frame = (rand, y, breite, 64)
        y += 74
        ergebnis.frame = (rand, y, breite, 56)
        y += 66
        knopf.frame = (rand, y, breite, 46)
        y += 56
        hinweis.frame = (rand, y, breite, 40)

    view.layout = layout
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
