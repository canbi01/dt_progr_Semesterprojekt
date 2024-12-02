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

# Bounding Boxes der Stützen abrufen
bounding_boxes = acc.Get3DBoundingBoxes(columns)

# Anzahl der Stützen mit der Element-ID "Baugespann" zählen und deren Koordinaten sowie Höhen ausgeben
count_columns_with_element_id = 0
for prop, bounding_box in zip(property_values, bounding_boxes):
    if prop.propertyValues[0].propertyValue.value == "Baugespann":
        count_columns_with_element_id += 1
        x_coord = bounding_box.boundingBox3D.xMin
        y_coord = bounding_box.boundingBox3D.yMin
        z_min = bounding_box.boundingBox3D.zMin
        z_max = bounding_box.boundingBox3D.zMax
        height = z_max - z_min
        print(f"Stütze mit Element-ID 'Baugespann': X = {x_coord}, Y = {y_coord}, Unterster Punkt = {z_min}, Oberster Punkt = {z_max}, Höhe = {height}")

# Gesamtergebnis ausgeben
print(f"Anzahl der Stützen mit der Element-ID 'Baugespann': {count_columns_with_element_id}")
