import xlsxwriter
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

    # Excel-Datei erstellen
    workbook = xlsxwriter.Workbook('Stuetzen_Liste.xlsx')
    worksheet = workbook.add_worksheet()

    # Kopfzeilen hinzufügen
    worksheet.write(0, 0, 'Element-ID')
    worksheet.write(0, 1, 'X-Koordinate')
    worksheet.write(0, 2, 'Y-Koordinate')
    worksheet.write(0, 3, 'MüM (Unterster Punkt)')
    worksheet.write(0, 4, 'Höhe der Stütze')

    # Daten der Stützen sammeln und in die Excel-Liste einfügen
    row = 1
    for prop, bounding_box in zip(property_values, bounding_boxes):
        if prop.propertyValues[0].propertyValue.value == "Baugespann":
            element_id = prop.propertyValues[0].propertyValue.value
            x_coord = round(bounding_box.boundingBox3D.xMin, 2)
            y_coord = round(bounding_box.boundingBox3D.yMin, 2)
            z_min = round(bounding_box.boundingBox3D.zMin, 2)
            z_max = round(bounding_box.boundingBox3D.zMax, 2)
            height = round(z_max - z_min, 2)

            # Daten in die Excel-Tabelle schreiben
            worksheet.write(row, 0, element_id)
            worksheet.write(row, 1, x_coord)
            worksheet.write(row, 2, y_coord)
            worksheet.write(row, 3, z_min)
            worksheet.write(row, 4, height)

            row += 1

    # Excel-Datei speichern
    workbook.close()

    # Gesamtergebnis ausgeben
    print(f"Excel-Liste 'Stuetzen_Liste.xlsx' wurde erfolgreich erstellt.")