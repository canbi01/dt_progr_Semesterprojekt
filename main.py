from V2.InterfaceV2 import main_interface
from V2.StuetzenAuswertenV2 import analyze_stuetzen
from V2.pdfGeneratorV2 import generate_pdf
import os

def main():
    # Öffne das Interface
    project_data, output_dir = main_interface()

    if not project_data or not output_dir:
        raise RuntimeError("Keine Projektdaten oder Zielverzeichnis verfügbar.")

    # Verbindung zu Archicad prüfen
    try:
        print("Starte Stützenanalyse...")
        data = analyze_stuetzen(project_data["Georeferenzierung"])
        print("Stützenanalyse abgeschlossen.")

        # PDF-Generierung
        print("Erstelle PDF...")
        pdf_file = os.path.join(output_dir, "Ausmass_Baugespann.pdf")
        generate_pdf(
            output_file=pdf_file,
            project_info=project_data,
            data=data
        )
        print(f"PDF erfolgreich erstellt: {pdf_file}")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
