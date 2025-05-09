# tasks/utils.py

def prioritaet_berechnen(titel):
    """
    Bestimmt automatisch die Priorität einer Aufgabe basierend auf Schlüsselwörtern im Titel.
    """
    titel = titel.lower()

    if any(wort in titel for wort in ['dringend', 'sofort', 'jetzt', 'wichtig', 'notfall']):
        return 'high'
    elif any(wort in titel for wort in ['bald', 'erledigen', 'wichtig']):
        return 'medium'
    elif any(wort in titel for wort in ['später', 'vielleicht', 'wenn zeit']):
        return 'low'
    else:
        return 'medium'


def detect_category(titel):
    """
    Erkennt automatisch die Kategorie einer Aufgabe basierend auf Schlüsselwörtern im Titel.
    """
    titel = titel.lower()

    if any(wort in titel for wort in ['meeting', 'besprechung', 'bericht', 'präsentation']):
        return 'Arbeit'
    elif any(wort in titel for wort in ['einkauf', 'supermarkt', 'rechnung', 'putzen']):
        return 'Haushalt'
    elif any(wort in titel for wort in ['sport', 'arzt', 'medikament', 'gesundheit']):
        return 'Gesundheit'
    else:
        return 'Sonstiges'

# tasks/utils.py

def aufgaben_empfehlung_berechnen(text):
    """
    Gibt eine Liste empfohlener Aufgaben basierend auf dem eingegebenen Text zurück.
    """
    text = text.lower()
    vorschlaege = []

    if 'einkaufen' in text:
        vorschlaege.append('Einkaufsliste erstellen')
    if 'fitness' in text or 'sport' in text:
        vorschlaege.append('30 Minuten Sport einplanen')
    if 'arzt' in text:
        vorschlaege.append('Arzttermin vereinbaren')
    if 'projekt' in text:
        vorschlaege.append('Projektzeit planen')
    if 'lesen' in text:
        vorschlaege.append('30 Minuten Lesen einplanen')

    return vorschlaege

