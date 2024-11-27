import requests
import json
import urllib.request as rq
from archicad import ACConnection

# Archicad API-Endpunkt (ersetze durch die korrekte URL deines Archicad-Servers)
ARCHICAD_API_URL = "http://localhost:19723"

# Funktion zum Abrufen aller Elemente und Filterung von Stützen (Schritt 1)
def get_all_columns():
    # Definiere die JSON-Anfrage für GetAllElements ohne ElementType-Filter
    payload = {
        "command": "GetAllElements"
    }
    # Sende die Anfrage an die Archicad API
    response = requests.post(ARCHICAD_API_URL, json=payload)
    # Antworte mit dem JSON-Inhalt
    data = response.json()
    # Debugging-Ausgabe: Alle Elemente anzeigen
    print("Empfangene Elemente:", json.dumps(data, indent=4))
    # Filtere die GUIDs der Elemente, die vom Typ "Column" sind
    column_guids = [element['guid'] for element in data.get('elements', []) if element.get('type') == "Column"]
    return column_guids

# Funktion zum Abrufen der Details einer spezifischen Stütze (Schritt 2)
def get_column_details(guid):
    # Definiere die JSON-Anfrage für GetElement mit einer spezifischen GUID
    payload = {
        "command": "GetElement",
        "parameters": {
            "elementId": {
                "guid": guid
            }
        }
    }
    # Sende die Anfrage an die Archicad API
    response = requests.post(ARCHICAD_API_URL, json=payload)
    # Antworte mit dem JSON-Inhalt (Details der Stütze)
    return response.json()

# Funktion zum Testen der Verbindung zur Archicad API
def check_api_is_alive():
    request = rq.Request(ARCHICAD_API_URL)
    response = rq.urlopen(request, json.dumps({
        "command": "API.IsAlive"
    }).encode("UTF-8"))
    result = json.loads(response.read())
    print("API IsAlive Response:", result)

# Beispiel für die Verwendung des offiziellen Archicad-Python-Pakets
def use_archicad_python_package():
    conn = ACConnection.connect()
    assert conn
    acc = conn.commands
    act = conn.types

    # Abrufen aller Spalten (Stützen)
    elements = acc.GetAllElements()
    column_elements = [element for element in elements if element.type.name == 'Column']

    print(f"Anzahl der Stützen (über die offizielle Archicad-Bibliothek): {len(column_elements)}")
    for column in column_elements:
        print("GUID der Stütze:", column.elementId.guid)

# Hauptprogramm zum Ausführen der Abfragen
if __name__ == "__main__":
    # Teste, ob die Archicad API erreichbar ist
    check_api_is_alive()

    # Schritt 1: Abrufen aller Stützen-GUIDs
    column_guids = get_all_columns()
    print(f"Anzahl der Stützen: {len(column_guids)}")
    
    # Schritt 2: Abrufen der Details der ersten Stütze, falls vorhanden
    if column_guids:
        first_column_details = get_column_details(column_guids[0])
        print("Details der ersten Stütze:")
        print(first_column_details)
    else:
        print("Keine Stützen im Modell gefunden.")

    # Verwende das Archicad-Python-Paket
    use_archicad_python_package()