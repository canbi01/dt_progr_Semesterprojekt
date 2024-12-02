# Verbindung Herstellen
from archicad import ACConnection
from typing import List, Tuple, Iterable

# Skript auslesen Stützen Archicad
import Prozessor.Stützen_Analyse as SA

if __name__ == "__main__":
    SA.start_app()

# Interface
import Prozessor.interface_final as inter

if __name__ == "__main__":
    inter.start_app()

# Verbindung zu Archicad herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."




