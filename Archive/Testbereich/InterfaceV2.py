import customtkinter as ctk
from tkinter import messagebox, filedialog

def main_interface():
    global current_project

    def verify_license():
        license_key = entry_license.get()
        if license_key == "123456":  # Beispiel für eine gültige Lizenz
            messagebox.showinfo("Lizenz gültig", "Lizenzprüfung erfolgreich!")
            root.destroy()  # Schließe die Lizenzprüfung
            project_selection()
        else:
            messagebox.showerror("Ungültige Lizenz", "Bitte geben Sie eine gültige Lizenznummer ein.")

    def project_selection():
        project_window = ctk.CTk()  # Neues Fenster für die Projektauswahl
        project_window.title("Projekt auswählen")

        label = ctk.CTkLabel(project_window, text="Projekt auswählen")
        label.pack(pady=10)

        # Beispiel-Projektliste
        example_projects = ["Gebäude A", "Gebäude B", "Gebäude C"]
        for project in example_projects:
            btn = ctk.CTkButton(
                project_window, text=project, 
                command=lambda p=project: open_project_window(p, project_window)
            )
            btn.pack(pady=5)

        project_window.mainloop()

    def open_project_window(project_name, parent_window):
        parent_window.destroy()  # Schließt das vorherige Fenster

        project_detail_window = ctk.CTk()  # Erstellt ein neues Hauptfenster
        project_detail_window.title(f"Details zu {project_name}")

        label_title = ctk.CTkLabel(project_detail_window, text=f"Projekt: {project_name}")
        label_title.grid(row=0, column=0, padx=10, pady=5)

        # Eingabefelder für die Projektinformationen
        labels = ["Parz:", "Adresse:", "Büro:", "Büro Adresse:", "Vorname Name:", "Adresse Bauherr:", "Ostausrichtung:", "Nordausrichtung:", "Höhe:", "Nordwinkel:"]
        entries = []
        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(project_detail_window, text=label_text)
            label.grid(row=i+1, column=0, padx=10, pady=5)
            entry = ctk.CTkEntry(project_detail_window)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            entries.append(entry)

        def save_project_details():
            project_details = {label_text: entry.get() for label_text, entry in zip(labels, entries)}
            print(f"Gespeicherte Details für {project_name}: {project_details}")
            messagebox.showinfo("Erfolg", "Projektdetails gespeichert!")

        save_button = ctk.CTkButton(project_detail_window, text="Speichern", command=save_project_details)
        save_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

        def open_baugespann_window():
            project_detail_window.destroy()  # Schließt das vorherige Fenster
            baugespann_window = ctk.CTk()  # Neues Fenster für Baugespann erstellen
            baugespann_window.title("Baugespann erstellen")

            label_instructions = ctk.CTkLabel(
                baugespann_window,
                text=(
                    "1. Navigieren Sie ins 3D-Fenster.\n"
                    "2. Öffnen Sie das Stützenwerkzeug und definieren Sie die Element-ID 'Baugespann'.\n"
                    "3. Platzieren Sie die Stützen an den gewünschten Gebäudeecken auf dem gewachsenen Terrain,\n"
                    "   und ziehen Sie die Stütze in die Höhe bis zur Gebäudeoberkante."
                ),
                justify="left",
            )
            label_instructions.pack(pady=10, padx=10)

            def enable_start_button():
                start_button.configure(state="normal")

            def execute_analysis():
                print("Stützenanalyse gestartet.")
                messagebox.showinfo("Erfolg", "Stützenanalyse abgeschlossen!")

            directory_button = ctk.CTkButton(
                baugespann_window, text="Verzeichnis auswählen", command=enable_start_button
            )
            directory_button.pack(pady=10)

            start_button = ctk.CTkButton(
                baugespann_window, text="Starten", command=execute_analysis, state="disabled"
            )
            start_button.pack(pady=10)

            close_baugespann_button = ctk.CTkButton(baugespann_window, text="Schließen", command=baugespann_window.destroy)
            close_baugespann_button.pack(pady=10)

            baugespann_window.mainloop()

        baugespann_button = ctk.CTkButton(project_detail_window, text="Baugespann erstellen", command=open_baugespann_window)
        baugespann_button.grid(row=len(labels)+2, column=0, columnspan=2, pady=10)

        close_button = ctk.CTkButton(project_detail_window, text="Schließen", command=project_detail_window.destroy)
        close_button.grid(row=len(labels)+3, column=0, columnspan=2, pady=10)

        project_detail_window.mainloop()

    # Lizenzprüfung GUI
    root = ctk.CTk()
    root.title("AEP-ArchicadEfficiencyProgramm")

    label_title = ctk.CTkLabel(root, text="Bitte tragen Sie Ihre Lizenznummer ein:")
    label_title.pack(pady=10)

    entry_license = ctk.CTkEntry(root, placeholder_text="Lizenznummer")
    entry_license.pack(pady=10)

    button_verify = ctk.CTkButton(root, text="Weiter", command=verify_license)
    button_verify.pack(pady=10)

    root.mainloop()

# Startpunkt des Skripts
if __name__ == "__main__":
    main_interface()
