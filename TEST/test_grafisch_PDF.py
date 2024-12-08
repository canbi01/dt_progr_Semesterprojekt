from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

def PDF_Vorlage(output_file, plankopf_daten, headers, data):
    page_width, page_height = landscape(A4)
    pdf = canvas.Canvas(output_file, pagesize=landscape(A4))
    pdf.setFont("Helvetica", 10)

    # Spalten und Zeilenstruktur
    spalten_start = [50, 250, 450, 650]  # X-Positionen der Spalten für den Plankopf
    table_start_x = 50  # Tabellenstart X
    table_start_y = page_height - 150  # Tabellenstart Y (unterhalb des Plankopfs)
    col_widths = [150, 150, 150, 150, 150]  # Breite der Tabellenspalten
    row_height = 20  # Zeilenhöhe
    plankopf_start_y = 50

    def draw_spalte(text, spalte_index, y_offset, font="Helvetica", size=10, bold=False):
        """
        Zeichnet Text in eine der definierten Spalten.
        """
        if bold:
            font = "Helvetica-Bold"
        pdf.setFont(font, size)
        x_position = spalten_start[spalte_index]
        pdf.drawString(x_position, y_offset, text)

    # Plankopf-Inhalte einfügen
    spalten_inhalte = [
        ("Bauherrschaft:", plankopf_daten["Bauherrschaft"], "Adresse Bauherrschaft:", plankopf_daten["Adresse_Bauherrschaft"]),
        ("Planummer:", plankopf_daten["Planummer"], "", ""),
        ("Projekt:", plankopf_daten["Projekt"], "Firma:", plankopf_daten["Firma"]),
        ("", "", "Adresse Firma:", plankopf_daten["Adresse_Firma"]),
    ]

    y_offset = plankopf_start_y
    for zeile in spalten_inhalte:
        for spalte_index, inhalt in enumerate(zeile):
            is_bold = spalte_index % 2 == 0  # Hervorheben der ersten und dritten Spalte jeder Zeile
            if inhalt.strip():
                draw_spalte(inhalt, spalte_index, y_offset, bold=is_bold)
        y_offset += row_height

    # Tabelle hinzufügen (Headers und Daten)
    pdf.setFont("Helvetica-Bold", 10)
    current_y = table_start_y
    for col_num, header in enumerate(headers):
        pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, header)
    pdf.setFont("Helvetica", 10)
    current_y -= row_height

    # Daten einfügen
    for row in data:
        for col_num, cell in enumerate(row):
            pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, str(cell))
        current_y -= row_height

    # PDF speichern
    pdf.save()

# Beispiel-Aufruf der Funktion
def main():
    plankopf_daten = {
        "Titel": "Visier Auszug Beispielobjekt",
        "Firma": "Testfirma",
        "Adresse_Firma": "Adresse Testfirma",
        "Planummer": "0001.GE-SI-Visier Auszug-001",
        "Projekt": "Beispielobjekt",
        "Bauherrschaft": "Bauherrschaft",
        "Adresse_Bauherrschaft": "Adresse Bauherrschaft",
    }
    headers = ['Element-ID', 'X-Koordinate', 'Y-Koordinate', 'MüM', 'Höhe']
    data = [
        ['123', '10.5', '20.3', '100.0', '15.0'],
        ['124', '11.0', '21.0', '101.0', '15.5'],
        ['125', '12.0', '22.0', '102.0', '16.0']
    ]
    output_file = "Stuetzen_Liste_Mit_Pankopf.pdf"
    PDF_Vorlage(output_file, plankopf_daten, headers, data)
    print(f"PDF '{output_file}' wurde erfolgreich erstellt.")

if __name__ == "__main__":
    main()
