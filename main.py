# Verbindung Herstellen
from archicad import ACConnection
from typing import List, Tuple, Iterable

# Interface
import interface_final

if __name__ == "__main__":
    interface_final.start_app()

# Verbindung zu Archicad herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

# Skript auslesen Stützen Archicad



