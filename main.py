# Verbindung Herstellen
from archicad import ACConnection
from typing import List, Tuple, Iterable

# Verbindung zu Archicad herstellen
conn = ACConnection.connect()
assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

# Auswählen Column Datei im Dokument
import column as cl

def start_func():
    #Hauptfunktion zum Ausführen

    print("Hauptprogramm gestartet")

    glb_conf_set = cl.read_source_data()
    #glb_conf_lst = glb_conf_set[0]
    #glb_conf_folder = glb_conf_set[1]

    #glb_export_lst = ifc_p.process_ifc_data(glb_conf_lst)
    #exp_p.export_data(glb_export_lst, glb_conf_lst, glb_conf_folder)


#Als Hauptprogramm ausführen
if _name_ == '_main_':
    start_func()