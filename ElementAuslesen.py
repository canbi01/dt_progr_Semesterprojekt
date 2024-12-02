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

# Zähle die Anzahl der Säulen, die sich auf der Ebene "000-Baugespann" befinden
count_columns_on_layer = 0
for column in columns:
    element_layer = acc.GetElementLayer(column.elementId)
    if element_layer.name == "000-Baugespann":
        count_columns_on_layer += 1

# Ausgabe der Anzahl der gefundenen Säulen auf der angegebenen Ebene
print(f"Number of Columns on Layer '000-Baugespann': {count_columns_on_layer}")





# Optional: Details zu den Säulen ausgeben
"""
for column in columns:
    print(f"Column ID: {column.elementId}")
"""

# ********* vo dene da une funktioniert au keine *********
"""
print(columns.attribut)

for colum in columns:
    print(f"die ELement-ID ist {columns.IFCLabel}")


stützen = act.GetElementClassifications("Baugespann")
print(f"id-hint: {stützen}")
"""