from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf(output_dir, project_details, headers, data):
    """
    Create a PDF report based on analyzed data and save it to the specified directory.

    :param output_dir: Target directory for the PDF
    :param project_details: Information about the selected project
    :param headers: Column headers for the table
    :param data: Table data
    """
    try:
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            raise RuntimeError(f"Output directory does not exist: {output_dir}")

        # Generate PDF file name
        project_name = project_details.get("Projekt", "Unbekanntes_Projekt")
        output_pdf = os.path.join(output_dir, f"Ausmass_Baugespann_{project_name}.pdf")

        # Setup PDF canvas
        page_width, page_height = landscape(A4)
        pdf = canvas.Canvas(output_pdf, pagesize=landscape(A4))
        pdf.setFont("Helvetica", 10)

        # Add project details header
        plankopf_start_y = page_height - 50
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, plankopf_start_y, "Projektdaten")

        plankopf_data = [
            ("Projekt:", project_details.get("Projekt", "N/A")),
            ("Parzelle:", project_details.get("Parzelle", "N/A")),
            ("Adresse:", project_details.get("Adresse", "N/A")),
            ("Büro:", project_details.get("Büro", "N/A")),
            ("Büro-Adresse:", project_details.get("Büro-Adresse", "N/A")),
            ("Bauherrschaft:", project_details.get("Bauherrschaft", {}).get("Name", "N/A")),
            ("Bauherr-Adresse:", project_details.get("Bauherrschaft", {}).get("Adresse", "N/A")),
        ]

        y_position = plankopf_start_y - 20
        for label, value in plankopf_data:
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(50, y_position, label)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(150, y_position, value)
            y_position -= 15

        # Add georeferencing data
        geo_data = [
            ("Ostausrichtung:", project_details.get("offsets", {}).get("Ostausrichtung", 0.0)),
            ("Nordausrichtung:", project_details.get("offsets", {}).get("Nordausrichtung", 0.0)),
            ("Höhe:", project_details.get("offsets", {}).get("Höhe", 0.0)),
            ("Nordwinkel:", f"{project_details.get('offsets', {}).get('Nordwinkel', 0.0)}°"),
        ]

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position - 10, "Georeferenzierung")
        y_position -= 25

        for label, value in geo_data:
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(50, y_position, label)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(150, y_position, str(value))
            y_position -= 15

        # Add date
        date_str = datetime.now().strftime("%d.%m.%Y")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(page_width - 150, plankopf_start_y, f"Ausgabedatum: {date_str}")

        # Add table headers
        table_start_x = 50
        table_start_y = y_position - 30
        pdf.setFont("Helvetica-Bold", 10)
        current_y = table_start_y
        col_widths = [150, 150, 150, 150, 150]

        for col_num, header in enumerate(headers):
            pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, header)

        pdf.setFont("Helvetica", 10)
        current_y -= 20

        # Add table data
        for row in data:
            for col_num, cell in enumerate(row):
                pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, str(cell))
            current_y -= 20

            # Add new page if necessary
            if current_y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                current_y = page_height - 50

                # Reprint headers on new page
                for col_num, header in enumerate(headers):
                    pdf.drawString(table_start_x + col_num * col_widths[col_num], current_y, header)
                current_y -= 20

        # Save PDF
        pdf.save()
        print(f"PDF wurde erfolgreich unter {output_pdf} gespeichert.")

    except Exception as e:
        raise RuntimeError(f"Fehler beim Erstellen der PDF: {e}")
