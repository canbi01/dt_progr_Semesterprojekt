from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from archicad import ACConnection
import xlsxwriter

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

# Funktion zur PDF-Erstellung mit Plankopf
def PDF_Vorlage(output_file, plankopf_daten, headers, data):
    page_width, page_height = landscape(A4)
    pdf = canvas.Canvas(output_file, pagesize=landscape(A4))
    pdf.setFont("Helvetica", 10)

    spalten_start = [50, 250, 450, 650]
    table_start_x = 50
    table_start_y = page_height - 250
    col_widths = [150, 150, 150, 150, 150]
    row_height = 20
    plankopf_start_y = page_height - 100

    def draw_spalte(text, spalte_index, y_offset, font="Helvetica", size=10, bold=False):
        if bold:
            font = "Helvetica-Bold"
        pdf.setFont(font, size)
        x_position = spalten_start[spalte_index]
        pdf.drawString(x_position, y_offset, text)

    spalten_inhalte = [
        ("Bauherrschaft:", plankopf_daten["Bauherrschaft"], "Adresse Bauherrschaft:", plankopf_daten["Adresse_Bauherrschaft"]),
        ("Planummer:", plankopf_daten["Planummer"], "", ""),
        ("Projekt:", plankopf_daten["Projekt"], "Firma:", plankopf_daten["Firma"]),
        ("", "", "Adresse Firma:", plankopf_daten["Adresse_Firma"]),
    ]

    y_offset = plankopf_start_y
    for zeile in spalten_inhalte:
        for spalte_index, inhalt in enumerate(zeile):
            is_bold = spalte_index % 2 == 0
            if inhalt.strip():
                draw_spalte(inhalt, spalte_index, y_offset, bold=is_bold)
        y_offset -= row_height

    pdf.setFont("Helvetica-Bold", 10)
    current_y = table_start_y
    for col_num, header in enumerate(headers):
        pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, header)
    pdf.setFont("Helvetica", 10)
    current_y -= row_height

    for row in data:
        for col_num, cell in enumerate(row):
            pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, str(cell))
        current_y -= row_height

    pdf.save()

# Funktion zur Analyse der Stützen
def analyze_stuetzen():
    try:
        conn = ACConnection.connect()
        assert conn, "Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft."

        acc = conn.commands
        act = conn.types
        acu = conn.utilities

        columns = acc.GetElementsByType("Column")
        element_id_property_id = acu.GetBuiltInPropertyId('General_ElementID')
        property_values = acc.GetPropertyValuesOfElements(columns, [element_id_property_id])
        bounding_boxes = acc.Get3DBoundingBoxes(columns)

        workbook = xlsxwriter.Workbook('Stuetzen_Liste.xlsx')
        worksheet = workbook.add_worksheet()

        headers = ['Element-ID', 'X-Koordinate (Vermessungspunkt)', 'Y-Koordinate (Vermessungspunkt)', 'MüM (Unterster Punkt)', 'Höhe der Stütze']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

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

                worksheet.write(row, 0, element_id)
                worksheet.write(row, 1, x_coord)
                worksheet.write(row, 2, y_coord)
                worksheet.write(row, 3, z_min)
                worksheet.write(row, 4, height)

                data.append([element_id, x_coord, y_coord, z_min, height])

                row += 1

        workbook.close()

        plankopf_daten = {
            "Bauherrschaft": "Bauherrschaft",
            "Adresse_Bauherrschaft": "Adresse Bauherrschaft",
            "Planummer": "1234",
            "Projekt": "Projektname",
            "Firma": "Firma",
            "Adresse_Firma": "Adresse Firma",
        }

        PDF_Vorlage("Stuetzen_Liste_Mit_Pankopf.pdf", plankopf_daten, headers, data)
        messagebox.showinfo("Erfolg", "Excel- und PDF-Dateien wurden erfolgreich erstellt.")

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler bei der Analyse: {e}")

# Hauptfenster erstellen
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Archicad Vermessungspunkt Interface")
root.geometry("600x400")

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

def save_inputs():
    global SURVEY_POINT_OFFSET_X, SURVEY_POINT_OFFSET_Y, SURVEY_POINT_OFFSET_Z
    try:
        SURVEY_POINT_OFFSET_X = float(entry_x.get())
        SURVEY_POINT_OFFSET_Y = float(entry_y.get())
        SURVEY_POINT_OFFSET_Z = float(entry_z.get())
        save_offsets()
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige numerische Werte ein.")

button_save = ctk.CTkButton(root, text="Offsets speichern", command=save_inputs)
button_save.pack(pady=10)

button_start = ctk.CTkButton(root, text="Analyse starten", command=analyze_stuetzen)
button_start.pack(pady=10)

root.mainloop()
