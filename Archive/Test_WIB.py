from archicad import ACConnection

def export_stuetzen_liste():
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

    # Kopfzeilen ausgeben
    print(f"{'Element-ID':<15} {'X-Koordinate':<15} {'Y-Koordinate':<15} {'MüM (Unterster Punkt)':<25} {'Höhe der Stütze':<20}")
    print("=" * 90)

    # Daten der Stützen sammeln und in die Konsole ausgeben
    for prop, bounding_box in zip(property_values, bounding_boxes):
        if prop.propertyValues[0].propertyValue.value == "Baugespann":
            element_id = prop.propertyValues[0].propertyValue.value
            x_coord = round(bounding_box.boundingBox3D.xMin, 2)
            y_coord = round(bounding_box.boundingBox3D.yMin, 2)
            z_min = round(bounding_box.boundingBox3D.zMin, 2)
            z_max = round(bounding_box.boundingBox3D.zMax, 2)
            height = round(z_max - z_min, 2)

            # Daten ausgeben
            print(f"{element_id:<15} {x_coord:<15} {y_coord:<15} {z_min:<25} {height:<20}")

    # Gesamtergebnis ausgeben
    print("\nStützen-Liste wurde erfolgreich in der Konsole ausgegeben.")

# Aufruf der Funktion
export_stuetzen_liste()
