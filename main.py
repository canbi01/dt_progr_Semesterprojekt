from V2.InterfaceV2 import main_interface
from V2.StuetzenAuswertenV2 import analyze_stuetzen
from V2.pdfGeneratorV2 import generate_pdf
import os

def main():
    # Starte die Haupt-Benutzeroberfläche
    license_key, current_project = main_interface()

    # Prüfe, ob ein Projekt ausgewählt wurde
    if not current_project:
        raise RuntimeError("Kein Projekt ausgewählt. Programm wird beendet.")

    # Verbindung zu Archicad herstellen und Stützen analysieren
    print(f"Starte Analyse für das Projekt: {current_project['name']}")
    offsets = current_project["offsets"]
    try:
        data = analyze_stuetzen(offsets)
    except RuntimeError as e:
        raise RuntimeError(f"Fehler bei der Stützenanalyse: {e}")

    # Generiere PDF basierend auf den Analyseergebnissen
    output_dir = os.path.join("outputs", current_project["name"])
    os.makedirs(output_dir, exist_ok=True)
    pdf_file = os.path.join(output_dir, "Stuetzen_Liste_Mit_Plankopf.pdf")
    try:
        generate_pdf(pdf_file, current_project, data)
        print(f"PDF erfolgreich erstellt: {pdf_file}")
    except RuntimeError as e:
        raise RuntimeError(f"Fehler beim Erstellen der PDF: {e}")

    print("Programm erfolgreich abgeschlossen.")

if __name__ == "__main__":
    main()
