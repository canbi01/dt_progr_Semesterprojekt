import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import xlsxwriter
from archicad import ACConnection
import pandas as pd
from fpdf import FPDF

# Globale Variablen für Vermessungspunkt-Offsets
SURVEY_POINT_OFFSET_X = 0.0
SURVEY_POINT_OFFSET_Y = 0.0
SURVEY_POINT_OFFSET_Z = 0.0

# Funktion zum Speichern der Offsets in einer Datei
def save_offsets():
    global SURVEY_POINT_OFFSET_X, SURVEY_POINT_OFFSET_Y, SURVEY_POINT_OFFSET_Z
    try:
        file_path = "survey_offsets.txt"
        with open(file_path, "w") as file:
            file.write(f"SURVEY_POINT_OFFSET_X={SURVEY_POINT_OFFSET_X}\n")
            file.write(f"SURVEY_POINT_OFFSET_Y={SURVEY_POINT_OFFSET_Y}\n")
            file.write(f"SURVEY_POINT_OFFSET_Z={SURVEY_POINT_OFFSET_Z}\n")
        messagebox.showinfo("Erfolg", f"Offsets erfolgreich in {file_path} gespeichert!")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Speichern der Offsets: {e}")

# Funktion zur Analyse der Stützen
def analyze_stuetzen():
    try:
        # Verbindung zu Archicad herstellen
        conn = ACConnection.connect()
        assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

        # Zugriff auf die Module für Befehle und Typen
        acc = conn.commands
        act = conn.types
        acu = conn.utilities

        # Alle Stützen-Elemente abrufen
        columns = acc.GetElementsByType("Column")

        # Built-in Property ID für die Element-ID abrufen
        element_id_property_id = acu.GetBuiltInPropertyId('General_ElementID')

        # Property-Werte für die abgerufenen Stützen-Elemente erhalten
        property_values = acc.GetPropertyValuesOfElements(columns, [element_id_property_id])

        # Bounding Boxes der Stützen abrufen
        bounding_boxes = acc.Get3DBoundingBoxes(columns)

        # Excel-Datei erstellen
        workbook = xlsxwriter.Workbook('Stuetzen_Liste.xlsx')
        worksheet = workbook.add_worksheet()

        # Kopfzeilen hinzufügen
        headers = ['Element-ID', 'X-Koordinate (Vermessungspunkt)', 'Y-Koordinate (Vermessungspunkt)', 'MüM (Unterster Punkt)', 'Höhe der Stütze']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Daten der Stützen sammeln und in die Excel-Liste einfügen
        data = []
        row = 1
        for prop, bounding_box in zip(property_values, bounding_boxes):
            if prop.propertyValues[0].propertyValue.value == "Baugespann":
                element_id = prop.propertyValues[0].propertyValue.value
                x_coord = round((bounding_box.boundingBox3D.xMin + bounding_box.boundingBox3D.xMax) / 2 - SURVEY_POINT_OFFSET_X, 2)
                y_coord = round((bounding_box.boundingBox3D.yMin + bounding_box.boundingBox3D.yMax) / 2 - SURVEY_POINT_OFFSET_Y, 2)
                z_min = round(bounding_box.boundingBox3D.zMin - SURVEY_POINT_OFFSET_Z, 2)
                z_max = round(bounding_box.boundingBox3D.zMax - SURVEY_POINT_OFFSET_Z, 2)
                height = round(z_max - z_min, 2)

                # Daten in die Excel-Tabelle schreiben
                worksheet.write(row, 0, element_id)
                worksheet.write(row, 1, x_coord)
                worksheet.write(row, 2, y_coord)
                worksheet.write(row, 3, z_min)
                worksheet.write(row, 4, height)

                # Daten für PDF sammeln
                data.append([element_id, x_coord, y_coord, z_min, height])

                row += 1

        # Excel-Datei speichern
        workbook.close()

        # PDF-Datei erstellen
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # PDF Kopfzeilen hinzufügen
        pdf.cell(200, 10, txt="Stützen Liste", ln=True, align='C')
        pdf.ln(10)

        # PDF Tabellenkopf hinzufügen
        for header in headers:
            pdf.cell(38, 10, txt=header, border=1, align='C')
        pdf.ln()

        # PDF Daten hinzufügen
        for row in data:
            for item in row:
                pdf.cell(38, 10, txt=str(item), border=1, align='C')
            pdf.ln()

        # PDF-Datei speichern
        pdf.output("Stuetzen_Liste.pdf")

        # Gesamtergebnis ausgeben
        messagebox.showinfo("Erfolg", "Excel- und PDF-Dateien wurden erfolgreich erstellt.")

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler bei der Analyse: {e}")

# Hauptfenster erstellen
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Archicad Vermessungspunkt Interface")
root.geometry("600x400")

# Anleitung
instructions = (
    "1. Öffnen Sie Ihr gewünschtes Archicad-File.\n"
    "2. Gehen Sie zu Verwaltung > Projekteinstellung > Lageeinstellungen und kopieren Sie die Vermessungspunkt-Koordinaten.\n"
    "3. Fügen Sie die Werte in die untenstehenden Felder ein.\n"
    "4. Wechseln Sie in die 3D-Ansicht und platzieren Sie die Stützen.\n"
    "5. Geben Sie 'Baugespann' bei der Element-ID ein.\n"
    "6. Klicken Sie auf 'Offsets speichern' und starten Sie die Analyse."
)
label_instructions = ctk.CTkLabel(root, text=instructions, justify="left", wraplength=550, font=("Arial", 14))
label_instructions.pack(pady=10)

# Eingabefelder für Vermessungspunkt
frame_inputs = ctk.CTkFrame(root)
frame_inputs.pack(pady=10, padx=10, fill="both", expand=True)

label_x = ctk.CTkLabel(frame_inputs, text="Vermessungspunkt X:")
label_x.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_x = ctk.CTkEntry(frame_inputs)
entry_x.grid(row=0, column=1, padx=5, pady=5)

label_y = ctk.CTkLabel(frame_inputs, text="Vermessungspunkt Y:")
label_y.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_y = ctk.CTkEntry(frame_inputs)
entry_y.grid(row=1, column=1, padx=5, pady=5)

label_z = ctk.CTkLabel(frame_inputs, text="Vermessungspunkt Z:")
label_z.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_z = ctk.CTkEntry(frame_inputs)
entry_z.grid(row=2, column=1, padx=5, pady=5)

# Funktionen für Schaltflächen
def save_inputs():
    global SURVEY_POINT_OFFSET_X, SURVEY_POINT_OFFSET_Y, SURVEY_POINT_OFFSET_Z
    try:
        SURVEY_POINT_OFFSET_X = float(entry_x.get())
        SURVEY_POINT_OFFSET_Y = float(entry_y.get())
        SURVEY_POINT_OFFSET_Z = float(entry_z.get())
        save_offsets()
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige numerische Werte ein.")

# Schaltflächen
button_save = ctk.CTkButton(root, text="Offsets speichern", command=save_inputs)
button_save.pack(pady=10)

button_start = ctk.CTkButton(root, text="Analyse starten", command=analyze_stuetzen)
button_start.pack(pady=10)

# Hauptfenster starten
root.mainloop()
