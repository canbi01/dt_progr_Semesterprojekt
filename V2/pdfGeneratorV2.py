from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

def generate_pdf(output_file, project_info, data):
    pdf = canvas.Canvas(output_file, pagesize=landscape(A4))
    pdf.setFont("Helvetica", 10)

    pdf.drawString(50, 500, f"Projekt: {project_info['Projekt']}")
    pdf.drawString(50, 480, f"Adresse: {project_info['Adresse']}")

    headers = ["Element-ID", "X-Koord", "Y-Koord", "MüM", "Höhe"]
    y = 450
    for header in headers:
        pdf.drawString(50, y, header)
        y -= 20

    for row in data:
        y -= 20
        for i, cell in enumerate(row):
            pdf.drawString(50 + i * 100, y, str(cell))

    pdf.save()
