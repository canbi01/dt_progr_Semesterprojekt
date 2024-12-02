# Verbindung Herstellen
from archicad import ACConnection
from typing import List, Tuple, Iterable


# Interface
import Prozessor.interface_final as inter

if __name__ == "__main__":
    inter.start_app()

# Verbindung zu Archicad herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."


# Test_main.py

# Die Datei archicad_export importieren
from Test_WIB import export_stuetzen_liste

# Eine beliebige Main-Funktion oder Logik, um das Skript zu starten
def main():
    # Stützenliste exportieren
    export_stuetzen_liste()

# Main aufrufen
if __name__ == "__main__":
    main()




