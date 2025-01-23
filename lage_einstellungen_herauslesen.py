from archicad import ACConnection

# Verbindung zur ArchiCAD API herstellen
try:
    ac_connection = ACConnection.connect()
    print("Verbindung zu ArchiCAD erfolgreich hergestellt!")
except Exception as e:
    print(f"Verbindung fehlgeschlagen: {e}")
    exit()

# Verfügbare Eigenschaften und Methoden von 'commands'
print("Verfügbare Attribute und Methoden in 'commands':")
print(dir(ac_connection.commands))

# Verfügbare Eigenschaften und Methoden von 'request'
print("Verfügbare Attribute und Methoden in 'request':")
print(dir(ac_connection.request))


# Georeferenzierungsdaten abrufen (wenn verfügbar)
try:
    response = ac_connection.request.get_location_settings()
    print("Georeferenzierungsdaten:")
    print(response)

except Exception as e:
    print(f"Fehler beim Abrufen der Georeferenzierung: {e}")

