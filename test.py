from archicad import ACConnection

# Verbindung zu Archicad herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

# Zugriff auf die Module für Befehle und Typen
acc = conn.commands
act = conn.types
acu = conn.utilities

# Test das die Verbindung funktioniert

walls = acc. GetElementsByType("Wall")

print(f"Number of Walls: {len(walls)}")

#Globale Variablen - Listen

column_lst = []


## Elemente finden und nummerieren
# Definiere den Ebenennamen, nach dem gesucht werden soll
target_layer_name = "200 Baugespann"  # Hier den Namen der gewünschten Ebene anpassen
 

 # Abrufen aller Elemente in ARCHICAD
all_elements = acc.GetAllElements()  # Alle Elemente laden

# Initialisierung der Liste für die Elemente auf der Ziel-Ebene
layer_elements = []


# Schleife über alle Elemente, um die Ebene zu filtern
for element in all_elements:
    # Hole die ID der allgemeinen Ebeneneigenschaft
    layer_property_id = acu.GetBuiltInPropertyId("Element ID")
    # Hole die Layer-Werte für das aktuelle Element
    element_layer = acc.GetPropertyValuesOfElements([element], [layer_property_id])

    # Prüfe, ob das Element auf der Ziel-Ebene liegt
    if element_layer[0].propertyValues[0].propertyValue.value == target_layer_name:
        layer_elements.append(element)

# Überprüfung, ob Elemente auf der Ziel-Ebene gefunden wurden
if not layer_elements:
    print(f"Keine Elemente auf der Ebene '{target_layer_name}' gefunden.")
else:
    # Liste für die Ausgabe der Ergebnisse
    output_data = []

    # Fortlaufende Nummerierung für jedes Element auf der Ebene "200 Baugespann"
    for i, element in enumerate(layer_elements, start=1):
        # Generiere eine neue ID, z.B. 'Baugespann_1', 'Baugespann_2', etc.
        new_id = f"Baugespann_{i}"