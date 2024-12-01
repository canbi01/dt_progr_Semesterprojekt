# ********* DIESES SCRIPT KANN ELEMENTE FILTRERN UND AUSLESEN *********

from archicad import ACConnection

# Verbindung zu Archicad herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

# Zugriff auf die Module für Befehle und Typen
acc = conn.commands
act = conn.types
acu = conn.utilities

# Säulen (Stützen) auslesen
columns = acc.GetElementsByType("Column")

# Ausgabe der Anzahl der gefundenen Säulen
print(f"Number of Columns: {len(columns)}")

# Optional: Details zu den Säulen ausgeben
for column in columns:
    print(f"Column ID: {column.elementId}")

