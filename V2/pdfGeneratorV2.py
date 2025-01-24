from archicad import ACConnection
import math

def load_offsets(project_offsets):
    try:
        return {
            "SURVEY_POINT_OFFSET_X": float(project_offsets.get("Ostausrichtung", 0.0)),
            "SURVEY_POINT_OFFSET_Y": float(project_offsets.get("Nordausrichtung", 0.0)),
            "SURVEY_POINT_OFFSET_Z": float(project_offsets.get("Höhe", 0.0)),
            "SURVEY_NORDWINKELOFFSET": float(project_offsets.get("Nordwinkel", 0.0))
        }
    except Exception as e:
        raise RuntimeError(f"Fehler beim Laden der Offsets: {e}")

def transform_coordinates(x, y, north_angle):
    angle_rad = math.radians(north_angle)
    return (
        x * math.cos(angle_rad) - y * math.sin(angle_rad),
        x * math.sin(angle_rad) + y * math.cos(angle_rad)
    )

def analyze_stuetzen(project_offsets):
    try:
        # Lade Offsets
        offsets = load_offsets(project_offsets)
        
        # Verbindung zu Archicad herstellen
        conn = ACConnection.connect()
        if not conn:
            raise RuntimeError("Keine Verbindung zu Archicad möglich.")

        acc = conn.commands
        acu = conn.utilities

        # Stützen (Columns) abrufen
        columns = acc.GetElementsByType("Column")
        if not columns:
            raise RuntimeError("Keine Stützen gefunden.")

        # Property-ID für Element-IDs abrufen
        element_id_property_id = acu.GetBuiltInPropertyId('General_ElementID')
        property_values = acc.GetPropertyValuesOfElements(columns, [element_id_property_id])
        bounding_boxes = acc.Get3DBoundingBoxes(columns)

        # Akzeptierte Element-IDs
        accepted_ids = {"Baugespann", "baugespan", "Baugespan", "baugespann"}
        
        data = []
        for prop, bounding_box in zip(property_values, bounding_boxes):
            element_id = prop.propertyValues[0].propertyValue.value
            if element_id not in accepted_ids:  # Prüfe auf akzeptierte IDs
                continue

            # Lokale Koordinaten berechnen
            local_x = (bounding_box.boundingBox3D.xMin + bounding_box.boundingBox3D.xMax) / 2
            local_y = (bounding_box.boundingBox3D.yMin + bounding_box.boundingBox3D.yMax) / 2

            # Globale Koordinaten mit Nordwinkel transformieren
            global_x, global_y = transform_coordinates(local_x, local_y, offsets["SURVEY_NORDWINKELOFFSET"])

            # Offset anwenden
            x_coord = round(global_x - offsets["SURVEY_POINT_OFFSET_X"], 2)
            y_coord = round(global_y - offsets["SURVEY_POINT_OFFSET_Y"], 2)
            z_min = round(bounding_box.boundingBox3D.zMin - offsets["SURVEY_POINT_OFFSET_Z"], 2)
            z_max = round(bounding_box.boundingBox3D.zMax - offsets["SURVEY_POINT_OFFSET_Z"], 2)
            height = round(z_max - z_min, 2)

            # Daten hinzufügen
            data.append([element_id, x_coord, y_coord, z_min, height])

        if not data:
            raise RuntimeError("Keine passenden Stützen gefunden.")

        return data

    except Exception as e:
        raise RuntimeError(f"Fehler bei der Stützenanalyse: {e}")