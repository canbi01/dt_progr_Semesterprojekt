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


import Prozessor.Stützen_Analyse

if __name__ == "__main__":
    try:
        subprocess.run(["python", "export_stuetzen.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Ausführung: {e}")




