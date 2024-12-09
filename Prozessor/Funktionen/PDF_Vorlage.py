from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

# Funktion zur PDF-Erstellung mit Plankopf
def PDF_Vorlage(output_file, plankopf_daten, headers, data):
    page_width, page_height = landscape(A4)
    pdf = canvas.Canvas(output_file, pagesize=landscape(A4))
    pdf.setFont("Helvetica", 10)

    spalten_start = [50, 250, 450, 650]
    table_start_x = 50
    table_start_y = page_height - 600
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

    
