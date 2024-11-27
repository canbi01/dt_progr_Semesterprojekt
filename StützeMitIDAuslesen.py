from archicad import ACConnection

# Verbindung zu Archicad herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

# Zugriff auf die Module für Befehle und Typen
acc = conn.commands
act = conn.types
acu = conn.utilities

# Säulen auslesen
columns = acc.GetElementsByType("Column")

# Filterung der Säulen, die das IFCLabel "Baugespann" als Attribut haben
filtered_columns = []

for column in columns:
    # Details zu den Eigenschaften des Elements abrufen 
    """
    s problem isch die eigeschafts abruefe/de befehl wos defür het nöd(GetElementClassifications())
    """
    classification_info = acc.GetElementClassifications(column.elementId)
    
    # Durchsuchen der Klassifikationen nach dem Attribut "Name (Baugespann)"
    for classification in classification_info:
        if classification.name == "Name" and classification.value == "Baugespann":
            filtered_columns.append(column)
            break

# Ausgabe der Anzahl der gefilterten Säulen
print(f"Number of Columns with 'Baugespann' as Name Attribute: {len(filtered_columns)}")

# Optional: Details zu den gefilterten Säulen ausgeben
for column in filtered_columns:
    print(f"Column ID: {column.elementId}")
