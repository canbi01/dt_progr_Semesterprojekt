from archicad import ACConnection
import math

def analyze_stuetzen(georeferenzierung):
    conn = ACConnection.connect()
    assert conn, "Keine Verbindung zu ARCHICAD möglich."

    acc = conn.commands
    acu = conn.utilities

    elements = acc.GetElementsByType("Column")
    bounding_boxes = acc.Get3DBoundingBoxes(elements)

    data = []
    for element, bbox in zip(elements, bounding_boxes):
        x_local = (bbox.boundingBox3D.xMin + bbox.boundingBox3D.xMax) / 2
        y_local = (bbox.boundingBox3D.yMin + bbox.boundingBox3D.yMax) / 2

        angle = math.radians(georeferenzierung["SURVEY_NORDWINKELOFFSET"])
        x_global = x_local * math.cos(angle) - y_local * math.sin(angle)
        y_global = x_local * math.sin(angle) + y_local * math.cos(angle)

        x_final = x_global - georeferenzierung["SURVEY_POINT_OFFSET_X"]
        y_final = y_global - georeferenzierung["SURVEY_POINT_OFFSET_Y"]
        z_min = bbox.boundingBox3D.zMin - georeferenzierung["SURVEY_POINT_OFFSET_Z"]
        z_max = bbox.boundingBox3D.zMax - georeferenzierung["SURVEY_POINT_OFFSET_Z"]

        data.append([element.elementId, x_final, y_final, z_min, z_max - z_min])

    return data
