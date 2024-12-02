from archicad import ACConnection

# Verbindung zur Archicad API herstellen
conn = ACConnection.connect()
assert conn, "Verbindung zu Archicad konnte nicht hergestellt werden."

acc = conn.commands
act = conn.types
acu = conn.utilities

################################ CONFIGURATION #################################
elements = acc.GetElementsByType('Column')
if not elements:
    print("Keine Stützen im Modell gefunden. Bitte sicherstellen, dass die Stützen im Modell vorhanden und sichtbar sind.")
    exit()

messageWhenNoConflictFound = "There is no elementID conflict."
conflictMessageParts = ["[Conflict]", "elements have", "as element ID:\n"]

def GetConflictMessage(elementIDPropertyValue, elementIds):
    return f"{conflictMessageParts[0]} {len(elementIds)} {conflictMessageParts[1]} '{elementIDPropertyValue}' {conflictMessageParts[2]}{sorted(elementIds, key=lambda id: id.guid)}"
################################################################################

# Abrufen der Eigenschaft 'General_ElementID'
try:
    elementIdPropertyId = acu.GetBuiltInPropertyId('General_ElementID')
except Exception as e:
    print(f"Fehler beim Abrufen der Eigenschaft 'General_ElementID': {e}")
    exit()

try:
    propertyValuesForElements = acc.GetPropertyValuesOfElements(elements, [elementIdPropertyId])
except Exception as e:
    print(f"Fehler beim Abrufen der Eigenschaftswerte der Stützen: {e}")
    exit()

# Dictionary zur Zuordnung von Element-IDs zu ihren Eigenschaftswerten
propertyValuesToElementIdsDictionary = {}
for i in range(len(propertyValuesForElements)):
    elementId = elements[i].elementId
    propertyValue = propertyValuesForElements[i].propertyValues[0].propertyValue.value if propertyValuesForElements[i].propertyValues[0].propertyValue else "UNDEFINED"
    if propertyValue not in propertyValuesToElementIdsDictionary:
        propertyValuesToElementIdsDictionary[propertyValue] = set()
    propertyValuesToElementIdsDictionary[propertyValue].add(elementId)

# Überprüfen auf Konflikte bei den Element-IDs
noConflictFound = True
for k, v in sorted(propertyValuesToElementIdsDictionary.items()):
    if len(v) > 1:
        noConflictFound = False
        print(GetConflictMessage(k, v))

if noConflictFound:
    print(messageWhenNoConflictFound)

# Abrufen der Höhen der Stützen
def get_column_heights():
    try:
        # Abrufen aller möglichen Eigenschafts-IDs
        allPropertyIds = acc.GetAllPropertyIds()
        heightPropertyId = None
        
        # Nach einer Eigenschaft suchen, die der Höhe entspricht
        for prop in allPropertyIds:
            if 'Height' in prop.propertyId or 'Höhe' in prop.propertyId:
                heightPropertyId = prop.propertyId
                break
        
        if not heightPropertyId:
            print("Keine Höhe-Eigenschaft gefunden.")
            return
        
        # Abrufen der Höhenwerte für die Stützen
        heightsForElements = acc.GetPropertyValuesOfElements(elements, [heightPropertyId])
        for i in range(len(heightsForElements)):
            elementId = elements[i].elementId.guid
            heightValue = heightsForElements[i].propertyValues[0].propertyValue.value if heightsForElements[i].propertyValues[0].propertyValue else "UNDEFINED"
            print(f"Höhe der Stütze mit GUID {elementId}: {heightValue}")
    except Exception as e:
        print(f"Fehler beim Abrufen der Höhen der Stützen: {e}")

# Abrufen der Höhen aller Stützen
get_column_heights()