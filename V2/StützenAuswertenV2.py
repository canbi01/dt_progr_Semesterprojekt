from archicad import ACConnection
import xlsxwriter
import os

# Globale Variablen für Vermessungspunkt-Offsets
SURVEY_POINT_OFFSET_X = 0.0
SURVEY_POINT_OFFSET_Y = 0.0
SURVEY_POINT_OFFSET_Z = 0.0

def load_offsets(file_path="survey_offsets.txt"):
    try:
        offsets = {"SURVEY_POINT_OFFSET_X": 0.0, "SURVEY_POINT_OFFSET_Y": 0.0, "SURVEY_POINT_OFFSET_Z": 0.0}
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                offsets[key] = float(value)
        return offsets
    except Exception as e:
        raise RuntimeError(f"Fehler beim Laden der Offsets: {e}")

#def load_offsets():
    """Liest die Vermessungspunkte aus der Datei 'survey_offsets.txt'."""
    global SURVEY_POINT_OFFSET_X, SURVEY_POINT_OFFSET_Y, SURVEY_POINT_OFFSET_Z
    try:
        with open("survey_offsets.txt", "r") as file:
            for line in file:
                if "SURVEY_POINT_OFFSET_X" in line:
                    SURVEY_POINT_OFFSET_X = float(line.split("=")[1])
                elif "SURVEY_POINT_OFFSET_Y" in line:
                    SURVEY_POINT_OFFSET_Y = float(line.split("=")[1])
                elif "SURVEY_POINT_OFFSET_Z" in line:
                    SURVEY_POINT_OFFSET_Z = float(line.split("=")[1])
    except Exception as e:
        raise RuntimeError(f"Fehler beim Laden der Vermessungspunkte: {e}")

from archicad import ACConnection
import xlsxwriter

from archicad import ACConnection
import xlsxwriter

def analyze_stuetzen(output_excel):
    try:
        # Offsets laden
        offsets = load_offsets()
        SURVEY_POINT_OFFSET_X = offsets["SURVEY_POINT_OFFSET_X"]
        SURVEY_POINT_OFFSET_Y = offsets["SURVEY_POINT_OFFSET_Y"]
        SURVEY_POINT_OFFSET_Z = offsets["SURVEY_POINT_OFFSET_Z"]

        conn = ACConnection.connect()
        assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

        acc = conn.commands
        act = conn.types
        acu = conn.utilities

        columns = acc.GetElementsByType("Column")
        element_id_property_id = acu.GetBuiltInPropertyId('General_ElementID')
        property_values = acc.GetPropertyValuesOfElements(columns, [element_id_property_id])
        bounding_boxes = acc.Get3DBoundingBoxes(columns)

        workbook = xlsxwriter.Workbook(output_excel)
        worksheet = workbook.add_worksheet()

        headers = ['Element-ID', 'X-Koordinate (VP)', 'Y-Koordinate (VP)', 'MüM (Unterster Punkt)', 'Höhe der Stütze']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        data = []
        row = 1
        for prop, bounding_box in zip(property_values, bounding_boxes):
            if prop.propertyValues[0].propertyValue.value == "Baugespann":
                element_id = prop.propertyValues[0].propertyValue.value
                x_coord = round((bounding_box.boundingBox3D.xMin + bounding_box.boundingBox3D.xMax) / 2 - SURVEY_POINT_OFFSET_X, 2)
                y_coord = round((bounding_box.boundingBox3D.yMin + bounding_box.boundingBox3D.yMax) / 2 - SURVEY_POINT_OFFSET_Y, 2)
                z_min = round(bounding_box.boundingBox3D.zMin - SURVEY_POINT_OFFSET_Z, 2)
                z_max = round(bounding_box.boundingBox3D.zMax - SURVEY_POINT_OFFSET_Z, 2)
                height = round(z_max - z_min, 2)

                worksheet.write(row, 0, element_id)
                worksheet.write(row, 1, x_coord)
                worksheet.write(row, 2, y_coord)
                worksheet.write(row, 3, z_min)
                worksheet.write(row, 4, height)

                data.append([element_id, x_coord, y_coord, z_min, height])

                row += 1

        workbook.close()
        return data

    except Exception as e:
        raise RuntimeError(f"Fehler bei der Stützenanalyse: {e}")