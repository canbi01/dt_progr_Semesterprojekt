from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf(output_dir, project_details, headers, data):
    try:
        if not os.path.exists(output_dir):
            raise RuntimeError(f"Output directory does not exist: {output_dir}")

        if not isinstance(project_details, dict):
            raise ValueError("project_details must be a dictionary.")

        project_name = project_details.get("Projekt", "Unbekanntes Projekt")
        output_pdf = os.path.join(output_dir, f"Ausmass_Baugespann_{project_name}.pdf")

        pdf = canvas.Canvas(output_pdf, pagesize=landscape(A4))
        pdf.setFont("Helvetica", 10)

        plankopf_start_y = 550
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, plankopf_start_y, "Projektdaten")

        plankopf_data = [
            ("Projektname:", project_details.get("Projekt", "N/A")),
            ("Parzelle:", project_details.get("Parzelle", "N/A")),
            ("Adresse:", project_details.get("Adresse", "N/A")),
            ("Projektverfasser:", project_details.get("Projektverfasser", "N/A")),
            ("Bauherrschaft:", project_details.get("Bauherrschaft", "N/A"))
        ]

        y_position = plankopf_start_y - 20
        for label, value in plankopf_data:
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(50, y_position, label)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(150, y_position, str(value))
            y_position -= 15

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y_position - 10, "")
        y_position -= 25

        table_start_x = 50
        current_y = y_position
        col_widths = [150, 150, 150, 150, 150]

        for col_num, header in enumerate(headers):
            pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, header)
        current_y -= 20

        pdf.setFont("Helvetica", 10)
        for row in data:
            for col_num, cell in enumerate(row):
                pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, str(cell))
            current_y -= 20

            if current_y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                current_y = 550

                for col_num, header in enumerate(headers):
                    pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, header)
                current_y -= 20

        pdf.save()
        print(f"PDF wurde erfolgreich unter {output_pdf} gespeichert.")

    except Exception as e:
        raise RuntimeError(f"Fehler beim Erstellen der PDF: {e}")
