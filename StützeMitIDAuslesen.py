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

# Built-in Property ID für die Element-ID abrufen
element_id_property_id = acu.GetBuiltInPropertyId('General_ElementID')

# Property-Werte für die abgerufenen Stützen-Elemente erhalten
property_values = acc.GetPropertyValuesOfElements(columns, [element_id_property_id])

# Anzahl der Stützen mit der Element-ID "Baugespann" zählen
count_columns_with_element_id = sum(
    1 for prop in property_values
    if prop.propertyValues[0].propertyValue.value == "Baugespann"
)

# Ergebnis ausgeben
print(f"Anzahl der Stützen mit der Element-ID 'Baugespann': {count_columns_with_element_id}")
