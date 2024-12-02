from archicad import ACConnection

# Verbindung zu Archicad herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

# Zugriff auf die Module für Befehle und Typen
acc = conn.commands
act = conn.types
acu = conn.utilities

# Alle Stützen-Elemente abrufen
columns = acc.GetElementsByType("Column")

# Built-in Property ID für den Layer-Namen abrufen
layer_property_id = acu.GetBuiltInPropertyId('ModelView_LayerName')

# Property-Werte für die abgerufenen Stützen-Elemente erhalten
property_values = acc.GetPropertyValuesOfElements(columns, [layer_property_id])

# Anzahl der Stützen auf dem Layer "000-Baugespann" zählen
count_columns_on_layer = sum(
    1 for prop in property_values
    if prop.propertyValues[0].propertyValue.value == "000-Baugespann"
)

# Ergebnis ausgeben
print(f"Anzahl der Stützen auf dem Layer '000-Baugespann': {count_columns_on_layer}")