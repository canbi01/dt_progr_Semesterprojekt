from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf(output_dir, project_details, headers, data):
    try:
        if not os.path.exists(output_dir):
            raise RuntimeError(f"Output directory does not exist: {output_dir}")

        # Set up PDF file name
        project_name = project_details.get("Projekt", "Unbekanntes_Projekt")
        output_pdf = os.path.join(output_dir, f"Ausmass_Baugespann_{project_name}.pdf")

        # Page settings
        page_width, page_height = landscape(A4)
        pdf = canvas.Canvas(output_pdf, pagesize=landscape(A4))
        pdf.setFont("Helvetica", 10)

        # Add logo and program name
        logo_x = page_width - 200
        logo_y = page_height - 50
        pdf.setFont("Helvetica-Bold", 36)
        pdf.drawString(logo_x, logo_y, "AEP")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(logo_x, logo_y - 20, "Archicad Efficiency Program")

        # Add project details
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, page_height - 100, "Projektdaten")
        plankopf_data = [
            ("Projektname:", project_details.get("Projekt", "N/A")),
            ("Parzelle:", project_details.get("Parzelle", "N/A")),
            ("Adresse:", project_details.get("Adresse", "N/A")),
            ("Projektverfasser:", project_details.get("Projektverfasser", "N/A")),
            ("Bauherrschaft:", project_details.get("Bauherrschaft", "N/A")),
        ]
        y_position = page_height - 120
        for label, value in plankopf_data:
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(50, y_position, label)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(150, y_position, str(value))
            y_position -= 15

        # Add the current date
        date_str = datetime.now().strftime("%d.%m.%Y")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(page_width - 150, page_height - 100, f"Ausgabedatum: {date_str}")

        # Add table headers
        table_start_x = 50
        table_start_y = y_position - 30
        pdf.setFont("Helvetica-Bold", 10)
        current_y = table_start_y
        column_widths = [100, 100, 100, 150, 150]  # Custom widths for better alignment

        for col_num, header in enumerate(headers):
            pdf.drawString(table_start_x + sum(column_widths[:col_num]), current_y, header)

        # Add table data
        pdf.setFont("Helvetica", 10)
        current_y -= 20
        for row in data:
            for col_num, cell in enumerate(row):
                pdf.drawString(table_start_x + sum(column_widths[:col_num]), current_y, str(cell))
            current_y -= 20

            # Add a new page if the current page is full
            if current_y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                current_y = page_height - 50

                # Re-add headers on the new page
                pdf.setFont("Helvetica-Bold", 10)
                for col_num, header in enumerate(headers):
                    pdf.drawString(table_start_x + sum(column_widths[:col_num]), current_y, header)
                current_y -= 20

        # Save the PDF
        pdf.save()
        print(f"PDF wurde erfolgreich unter {output_pdf} gespeichert.")

    except Exception as e:
        raise RuntimeError(f"Fehler beim Erstellen der PDF: {e}")
