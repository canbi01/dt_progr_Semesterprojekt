from archicad import ACConnection
import math
import os


def load_offsets(project_offsets):
    """
    Lädt die Offsets aus den Projektdaten.

    :param project_offsets: Dictionary mit Offset-Werten
    :return: Dictionary mit geladenen Offsets
    """
    try:
        offsets = {
            "SURVEY_POINT_OFFSET_X": float(project_offsets.get("Ostausrichtung", 0.0)),
            "SURVEY_POINT_OFFSET_Y": float(project_offsets.get("Nordausrichtung", 0.0)),
            "SURVEY_POINT_OFFSET_Z": float(project_offsets.get("Höhe", 0.0)),
            "SURVEY_NORDWINKELOFFSET": float(project_offsets.get("Nordwinkel", 0.0)),
        }
        return offsets
    except Exception as e:
        raise RuntimeError(f"Fehler beim Laden der Offsets: {e}")


def transform_coordinates(x, y, north_angle):
    """
    Transformiert die lokalen Koordinaten unter Berücksichtigung der Nordrichtung.

    :param x: Lokale X-Koordinate
    :param y: Lokale Y-Koordinate
    :param north_angle: Winkel der Nordrichtung in Grad
    :return: Transformierte X- und Y-Koordinaten
    """
    angle_rad = math.radians(north_angle)
    transformed_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    transformed_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return transformed_x, transformed_y


def analyze_stuetzen(project_offsets):
    """
    Analysiert Stützen in der Archicad-Datei und gibt die Ergebnisse für die PDF-Generierung zurück.

    :param project_offsets: Offsets für die Georeferenzierung aus dem Projekt
    :return: Liste der analysierten Stützen mit ihren Koordinaten und Höhen
    """
    try:
        offsets = load_offsets(project_offsets)
        SURVEY_POINT_OFFSET_X = offsets["SURVEY_POINT_OFFSET_X"]
        SURVEY_POINT_OFFSET_Y = offsets["SURVEY_POINT_OFFSET_Y"]
        SURVEY_POINT_OFFSET_Z = offsets["SURVEY_POINT_OFFSET_Z"]
        SURVEY_NORDWINKELOFFSET = offsets["SURVEY_NORDWINKELOFFSET"]

        conn = ACConnection.connect()
        assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

        acc = conn.commands
        act = conn.types
        acu = conn.utilities

        columns = acc.GetElementsByType("Column")
        element_id_property_id = acu.GetBuiltInPropertyId('General_ElementID')
        property_values = acc.GetPropertyValuesOfElements(columns, [element_id_property_id])
        bounding_boxes = acc.Get3DBoundingBoxes(columns)

        data = []
        for prop, bounding_box in zip(property_values, bounding_boxes):
            if prop.propertyValues[0].propertyValue.value == "Baugespann":
                element_id = prop.propertyValues[0].propertyValue.value

                # Lokale Koordinaten berechnen
                local_x = (bounding_box.boundingBox3D.xMin + bounding_box.boundingBox3D.xMax) / 2
                local_y = (bounding_box.boundingBox3D.yMin + bounding_box.boundingBox3D.yMax) / 2

                # Transformation der Koordinaten mit Nordrichtung
                global_x, global_y = transform_coordinates(local_x, local_y, SURVEY_NORDWINKELOFFSET)

                # Offset anwenden
                x_coord = round(global_x - SURVEY_POINT_OFFSET_X, 2)
                y_coord = round(global_y - SURVEY_POINT_OFFSET_Y, 2)
                z_min = round(bounding_box.boundingBox3D.zMin - SURVEY_POINT_OFFSET_Z, 2)
                z_max = round(bounding_box.boundingBox3D.zMax - SURVEY_POINT_OFFSET_Z, 2)
                height = round(z_max - z_min, 2)

                # Ergebnisse speichern
                data.append([element_id, x_coord, y_coord, z_min, height])

        return data

    except Exception as e:
        raise RuntimeError(f"Fehler bei der Stützenanalyse: {e}")
