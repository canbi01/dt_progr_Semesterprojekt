from archicad import ACConnection
import V2.InterfaceV2 as Interface
import V2.StützenAuswertenV2 as Stuetzen
import V2.pdfGeneratorV2 as PDF
import os
from V2.StützenAuswertenV2 import analyze_stuetzen

def main():
    # Das Interface wird automatisch gestartet, wenn das Modul importiert wird.
    
    # Zielverzeichnis und Offsets aus Interface erhalten
    output_dir = Interface.output_directory
    if not output_dir:
        raise RuntimeError("Kein Zielverzeichnis ausgewählt. Bitte starten Sie das Programm neu.")

    # Verbindung zu Archicad herstellen
    conn = ACConnection.connect()
    if not conn:
        raise RuntimeError("Keine Verbindung zu ARCHICAD möglich. Bitte sicherstellen, dass ARCHICAD läuft.")
    print("Erfolgreich mit Archicad verbunden.")

    # Schritt 2: Stützenanalyse durchführen
    try:
        print("Starte Stützenanalyse...")
        excel_file = os.path.join(output_dir, "Stuetzen_Liste.xlsx")
        data = Stuetzen.analyze_stuetzen(output_excel=excel_file)
        print(f"Stützenanalyse abgeschlossen. Ergebnisse in {excel_file} gespeichert.")
    except Exception as e:
        raise RuntimeError(f"Fehler bei der Stützenanalyse: {e}")

    # Schritt 3: PDF erstellen
    try:
        print("Erstelle PDF...")
        plankopf_daten = {
            "Bauherrschaft": "Bauherrschaft",
            "Adresse_Bauherrschaft": "Adresse der Bauherrschaft",
            "Planummer": "1234",
            "Projekt": "Projektname",
            "Firma": "Ihre Firma",
            "Adresse_Firma": "Adresse der Firma",
        }
        pdf_file = os.path.join(output_dir, "Stuetzen_Liste_Mit_Plankopf.pdf")
        headers = ['Element-ID', 'X-Koordinate (VP)', 'Y-Koordinate (VP)', 'Müm (Unterster Punkt)', 'Höhe der Stütze']
        PDF.generate_pdf(output_dir=output_dir, plankopf_daten=plankopf_daten, headers=headers, data=data)
        print(f"PDF erfolgreich erstellt und gespeichert unter {pdf_file}.")
    except Exception as e:
        raise RuntimeError(f"Fehler beim Erstellen der PDF: {e}")

    print("Programm erfolgreich abgeschlossen.")

if __name__ == "__main__":
    main()