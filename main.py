import os
from archicad import ACConnection
import V2.InterfaceV2 as Interface
import V2.StuetzenAuswertenV2 as Stuetzen
import V2.pdfGeneratorV2 as PDF
from tkinter import messagebox

def main():
    try:
        # Step 1: License Verification
        license_key = Interface.start_license_verification()
        if license_key != "123456":
            raise RuntimeError("Ungültige Lizenznummer. Das Programm wird beendet.")

        # Step 2: Project Selection
        project = Interface.select_project_interface()
        if not project:
            raise RuntimeError("Kein Projekt ausgewählt. Bitte starten Sie das Programm neu.")

        project_name = project.get("name", "Unbekanntes Projekt")
        project_details = project.get("details", {})

        print(f"DEBUG: project = {project}")
        print(f"DEBUG: project_details = {project_details}")

        # Step 3: Shortcut Selection
        selected_shortcut = Interface.select_shortcut()
        if selected_shortcut != "Ausmass Baugespann":
            print("Shortcut nicht implementiert. Das Programm wird beendet.")
            return

        # Step 4: Archicad Connection
        conn = ACConnection.connect()
        if not conn:
            Interface.show_error("Archicad Verbindung fehlgeschlagen. Bitte Archicad erneut öffnen.")
            return

        print(f"Erfolgreich mit Archicad verbunden für Projekt {project_name}.")

        # Step 5: Instructions
        Interface.show_analysis_instructions(project_name)

        # Step 6: Output Directory Selection
        output_dir = Interface.select_output_directory()
        if not output_dir:
            raise RuntimeError("Kein Zielverzeichnis ausgewählt. Bitte starten Sie das Programm neu.")

        # Step 7: Stützen Analysis
        print("Starte Stützenanalyse...")
        data = Stuetzen.analyze_stuetzen(project_details)
        print("Stützenanalyse abgeschlossen.")

        # Step 8: PDF Generation
        print("Erstelle PDF...")
        project_details["Projektname"] = project_name  # Sicherstellen, dass der Projektname übergeben wird
        headers = ['Element-ID', 'X-Koordinate (VP)', 'Y-Koordinate (VP)', 'Müm (unterster Punkt)', 'Höhe der Stütze']
        PDF.generate_pdf(output_dir, project_details, headers, data)
        success_message = f"PDF erfolgreich erstellt und gespeichert in {output_dir}."
        print(success_message)

        # Show success message in a popup
        messagebox.showinfo("PDF-Erstellung", success_message)

        print("Programm erfolgreich abgeschlossen.")

    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()