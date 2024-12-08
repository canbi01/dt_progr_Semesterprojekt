# Verbindung Herstellen
from archicad import ACConnection
from typing import List, Tuple, Iterable

# Interface
import Prozessor.test_interface as inter

if __name__ == "__main__":
    inter.start_app()

# Verbindung zu Archicad herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

# Analyse Druchführen
import Prozessor.test_Alles 




