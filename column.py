import pandas as pd
import os
import Helpers.Data_Helpers as hlp

#Globale Variablen - Listen

conf_lst = []

#Generate Filter Form

def read_source_data():

    #Alle Grundlagen einlesen > IFC + Excel-Elementplan

    print("Start: Starte Grunddatein einlesen...")

    source_folder = input("Pfad zum Basisordner eingeben >>> ")
    xls_file_name = "Elementplan.xlsx"
    xls_file = os.path.join(source_folder, xls_file_name)

    check_file = os.path.isfile(xls_file)

    #print(check_file)

    if(check_file):

        s_data_category = pd.read_excel(xls_file, "Objektkatalog")
        s_data_attributes = pd.read_excel(xls_file, "Attributsliste")

        #Daten aus dem Elementplan auslesen und strukturiert speichern

        col_count = len(s_data_category.columns)

        for index, row in s_data_category.iterrows():  

            if col_count > 3:  
        
                for gr in range(3,col_count):
                    attr_group_conf = s_data_category.iloc[index,gr]
                    
                    if(str(attr_group_conf).lower() == "x"):
                        current_attr_in_group = s_data_attributes[s_data_attributes["Gruppe"] == s_data_category.columns[gr]]
                        print(current_attr_in_group)               
                        
                        prop_lst = []

                        for _i, _r in current_attr_in_group.iterrows():

                            p_h = hlp.Prop_Holder(_r["Pset"], _r["Property"], _r["Gruppe"])
                            prop_lst.append(p_h)            

                        _target_obj = hlp.filterConfig(row["Branch"], conf_lst)

                        if _target_obj != None:

                            print("Adding to Configuration: ")
                            print("Klasse: " + row["IfcClass"])

                            _target_obj.prop_list.extend(prop_lst)

                        else:
                            print("Creating Configuration: ")
                            print("Klasse: " + row["IfcClass"])    

                            d_h = hlp.Data_Holder(row["IfcClass"], prop_lst, row["Branch"], row["Quelle"], source_folder)
                            conf_lst.append(d_h)

                        print("Finished Creating Configuration")

        return (conf_lst, source_folder)


## Elemente finden und nummerieren
# Definiere den Ebenennamen, nach dem gesucht werden soll
target_layer_name = "200 Baugespann"  # Hier den Namen der gewünschten Ebene anpassen

# Abrufen aller Elemente in ARCHICAD
all_elements = acc.GetAllElements()  # Alle Elemente laden

# Initialisierung der Liste für die Elemente auf der Ziel-Ebene
layer_elements = []


# Schleife über alle Elemente, um die Ebene zu filtern
for element in all_elements:
    # Hole die ID der allgemeinen Ebeneneigenschaft
    layer_property_id = acu.GetBuiltInPropertyId("General_Layer")
    # Hole die Layer-Werte für das aktuelle Element
    element_layer = acc.GetPropertyValuesOfElements([element], [layer_property_id])

    # Prüfe, ob das Element auf der Ziel-Ebene liegt
    if element_layer[0].propertyValues[0].propertyValue.value == target_layer_name:
        layer_elements.append(element)

# Überprüfung, ob Elemente auf der Ziel-Ebene gefunden wurden
if not layer_elements:
    print(f"Keine Elemente auf der Ebene '{target_layer_name}' gefunden.")
else:
    # Liste für die Ausgabe der Ergebnisse
    output_data = []

    # Fortlaufende Nummerierung für jedes Element auf der Ebene "200 Baugespann"
    for i, element in enumerate(layer_elements, start=1):
        # Generiere eine neue ID, z.B. 'Baugespann_1', 'Baugespann_2', etc.
        new_id = f"Baugespann_{i}"
        
        # Setze die Element-ID unter der Klassifizierung "General_ElementID"
        acc.SetElementProperties(
            [element.elementId],
            [act.ElementIdProperty("General_ElementID", new_id)]
        )

## Koordinaten x, y, z auslesen
 # Abrufen der Geometrie für das aktuelle Element
        geometry_property_id = acu.GetBuiltInPropertyId("General_Geometry")
        geometry_data = acc.GetPropertyValuesOfElements([element], [geometry_property_id])

        # Koordinaten extrahieren
        if geometry_data and geometry_data[0].propertyValues:
            coordinates = geometry_data[0].propertyValues[0].propertyValue.value
            # Die Koordinaten sind oft in Form von Punkten (x, y, z)
            x, y, z = coordinates.x, coordinates.y, coordinates.z
            
            # Hier speichern wir die tiefsten und höchsten Z-Koordinaten
            if i == 1:
                min_z = max_z = z  # Initialisierung mit der ersten Z-Koordinate
            else:
                min_z = min(min_z, z)
                max_z = max(max_z, z)

            # Ausgabe der Koordinaten
            print(f"Element {new_id} hat Koordinaten: X={x}, Y={y}, Z={z}")

##