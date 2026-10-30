# iFit Code

Kleiner Rechner für den **Privileged Mode** auf iFit-/NordicTrack-Konsolen.

Die Konsole zeigt eine sechsstellige Zahl und verlangt eine Antwort. Die Antwort
wird nicht bei iFit erfragt, sondern lässt sich berechnen: die angezeigte Zahl
ist der Startwert des Java-Zufallsgenerators.

```java
long responseCode = new Random((long) Integer.parseInt(iFitCode)).nextInt(999999);
```

Beispiel: `123456` → `382410`

## Benutzung

1. Seite öffnen (oder vom Home-Bildschirm starten)
2. Die Zahl von der Konsole eintippen
3. Die angezeigte Antwort auf der Konsole eintippen

Die Seite rechnet lokal im Browser. Kein Server, keine Übertragung, keine
Speicherung.

## Aufs Telefon legen

- **iPhone:** in Safari öffnen → Teilen → *Zum Home-Bildschirm*
- **Android:** in Chrome öffnen → Menü → *Zum Startbildschirm hinzufügen*

Nach dem ersten Aufruf liegt die Seite im Cache und startet auch ohne Netz.

## Ablauf auf der Konsole

1. Gerät normal hochfahren, bis das Bild fertig ist
2. Freie Fläche **oben links** suchen
3. **10-mal** antippen
4. **7 Sekunden** warten
5. Dieselbe Stelle **nochmals 10-mal** antippen
6. Fenster mit sechsstelliger Zahl erscheint

Der Zugang gilt nur bis zum nächsten Neustart.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | die Seite (HTML, CSS und JavaScript in einer Datei) |
| `ifit-icon.png` | Symbol für den Home-Bildschirm |
| `manifest.json` | macht die Seite installierbar |
| `sw.js` | Service Worker, legt die Seite offline ab |

## Hintergrund

Die Rechnung stammt aus der NordicTrack-Gemeinschaft und ist seit Jahren
öffentlich dokumentiert. Sie ist kein Geheimnis und kein Umgehen eines
Passworts – sie ersetzt lediglich einen Anruf beim Support.

Der Privileged Mode ist für Servicetechnik gedacht. An Geräten mit Motoren
gilt: Umsicht walten lassen.

Lizenz: GPL-3.0 (passend zum Hauptprojekt).
