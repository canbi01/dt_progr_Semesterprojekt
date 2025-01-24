from archicad import ACConnection
import math

# Load offsets from project details
def load_offsets(project_offsets):
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

# Transform local coordinates based on north angle
def transform_coordinates(x, y, north_angle):
    angle_rad = math.radians(north_angle)
    transformed_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    transformed_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return transformed_x, transformed_y

# Analyze columns (Stützen) in Archicad
def analyze_stuetzen(project_offsets):
    try:
        # Load offsets
        offsets = load_offsets(project_offsets)
        SURVEY_POINT_OFFSET_X = offsets["SURVEY_POINT_OFFSET_X"]
        SURVEY_POINT_OFFSET_Y = offsets["SURVEY_POINT_OFFSET_Y"]
        SURVEY_POINT_OFFSET_Z = offsets["SURVEY_POINT_OFFSET_Z"]
        SURVEY_NORDWINKELOFFSET = offsets["SURVEY_NORDWINKELOFFSET"]

        # Connect to Archicad
        conn = ACConnection.connect()
        if not conn:
            raise RuntimeError("Keine Verbindung zu Archicad möglich. Bitte sicherstellen, dass Archicad läuft.")

        acc = conn.commands
        acu = conn.utilities

        # Retrieve all columns
        columns = acc.GetElementsByType("Column")
        if not columns:
            raise RuntimeError("Keine Stützen (Columns) in der Archicad-Datei gefunden.")

        # Retrieve Element IDs and Bounding Boxes
        element_id_property_id = acu.GetBuiltInPropertyId('General_ElementID')
        property_values = acc.GetPropertyValuesOfElements(columns, [element_id_property_id])
        bounding_boxes = acc.Get3DBoundingBoxes(columns)

        data = []

        # Process each column
        for prop, bounding_box in zip(property_values, bounding_boxes):
            # Filter by Element ID "Baugespann"
            element_id = prop.propertyValues[0].propertyValue.value
            if element_id != "Baugespann":
                continue

            # Calculate local coordinates
            local_x = (bounding_box.boundingBox3D.xMin + bounding_box.boundingBox3D.xMax) / 2
            local_y = (bounding_box.boundingBox3D.yMin + bounding_box.boundingBox3D.yMax) / 2

            # Transform coordinates with north angle
            global_x, global_y = transform_coordinates(local_x, local_y, SURVEY_NORDWINKELOFFSET)

            # Apply offsets
            x_coord = round(global_x - SURVEY_POINT_OFFSET_X, 2)
            y_coord = round(global_y - SURVEY_POINT_OFFSET_Y, 2)
            z_min = round(bounding_box.boundingBox3D.zMin - SURVEY_POINT_OFFSET_Z, 2)
            z_max = round(bounding_box.boundingBox3D.zMax - SURVEY_POINT_OFFSET_Z, 2)
            height = round(z_max - z_min, 2)

            # Append results
            data.append([element_id, x_coord, y_coord, z_min, height])

        if not data:
            raise RuntimeError("Keine passenden Stützen gefunden (Element-ID: 'Baugespann').")

        return data

    except Exception as e:
        raise RuntimeError(f"Fehler bei der Stützenanalyse: {e}")