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
    attributes = acc.GetElementAttributes(column.elementId)
    layer_name = next((attr.value for attr in attributes.attributeValues if attr.attributeId.attributeType == 'Layer'), None)
    if layer_name == "000-Baugespann":
        count_columns_on_layer += 1

# Ausgabe der Anzahl der gefundenen Säulen auf der angegebenen Ebene
print(f"Number of Columns on Layer '000-Baugespann': {count_columns_on_layer}")
