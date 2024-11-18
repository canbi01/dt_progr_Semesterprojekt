import pandas as pd
import os
import Helpers.Data_Helpers as hlp

from archicad import ACConnection
from typing import List, Tuple, Iterable

# Verbindung zu ARCHICAD herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."


# Zugriff auf die Module für Befehle und Typen
acc = conn.commands
act = conn.types
acu = conn.utilities

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
    layer_property_id = acu.GetBuiltInPropertyId("General_Layer")
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
        
        # Setze die Element-ID unter der Klassifizierung "General_ElementID"
        acc.SetElementProperties(
            [element.elementId],
            [act.ElementIdProperty("General_ElementID", new_id)]
        )

## Koordinaten x, y, z auslesen
 # Abrufen der Geometrie für das aktuelle Element
        geometry_property_id = acu.GetBuiltInPropertyId("General_Geometry")
        geometry_data = acc.GetPropertyValuesOfElements([element], [geometry_property_id])

        # Koordinaten extrahieren
        if geometry_data and geometry_data[0].propertyValues:
            coordinates = geometry_data[0].propertyValues[0].propertyValue.value
            # Die Koordinaten sind oft in Form von Punkten (x, y, z)
            x, y, z = coordinates.x, coordinates.y, coordinates.z
            
            # Hier speichern wir die tiefsten und höchsten Z-Koordinaten
            if i == 1:
                min_z = max_z = z  # Initialisierung mit der ersten Z-Koordinate
            else:
                min_z = min(min_z, z)
                max_z = max(max_z, z)

            # Ausgabe der Koordinaten
            print(f"Element {new_id} hat Koordinaten: X={x}, Y={y}, Z={z}")

##