from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf(output_path, project_data, stuetzen_data):
    """
    Generiert ein PDF mit Projektdaten und Stützenanalyse.
    """
    pdf = canvas.Canvas(output_path, pagesize=landscape(A4))
    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 550, f"Projekt: {project_data['name']}")
    pdf.drawString(50, 530, f"Adresse: {project_data['details']['Adresse']}")
    pdf.drawString(50, 510, f"Büro: {project_data['details']['Büro']}")
    pdf.drawString(50, 490, f"Ausgabedatum: {datetime.now().strftime('%d.%m.%Y')}")

    table_start_y = 450
    headers = ["Element ID", "X-Koordinate (VP)", "Y-Koordinate (VP)", "MüM", "Höhe"]
    for i, header in enumerate(headers):
        pdf.drawString(50 + i * 100, table_start_y, header)

    y = table_start_y - 20
    for row in stuetzen_data:
        for i, cell in enumerate(row):
            pdf.drawString(50 + i * 100, y, str(cell))
        y -= 20

    pdf.save()
