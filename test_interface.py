import customtkinter as ctk
from tkinter import messagebox, filedialog, simpledialog, ttk
import os
import subprocess

# Funktionen und GUI
def start_app():
    # Hauptfenster erstellen
    ctk.set_appearance_mode("Dark")  # Dark mode für modernes Aussehen
    ctk.set_default_color_theme("dark-blue")  # Setze ein Farbschema

    root = ctk.CTk()
    root.title("Projektverwaltung")
    root.geometry("1200x700")  # Breiteres Fenster für zusätzliche Spalte
    root.resizable(True, True)  # Fenstergröße anpassbar machen

    # Variable, um den Status der geöffneten Datei zu verfolgen
    archicad_datei_geoeffnet = [False]  # Verwende eine Liste, um den veränderlichen Status beizubehalten

    # Funktionen
    def login():
        benutzername = entry_email.get()
        passwort = entry_password.get()
        
        if benutzername == "admin" and passwort == "123":
            for widget in root.winfo_children():
                widget.destroy()  # Löscht alle Widgets im Fenster
            neue_benutzeroberflaeche()
        else:
            messagebox.showerror("Fehler", "Falscher Benutzername oder falsches Passwort")

    def neue_benutzeroberflaeche():
        # Löscht alle Widgets im Fenster
        for widget in root.winfo_children():
            widget.destroy()
        
        frame_main = ctk.CTkFrame(root)
        frame_main.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        frame_right = ctk.CTkFrame(root, width=300)
        frame_right.grid(row=0, column=1, padx=10, pady=20, sticky="ns")

        root.grid_columnconfigure(0, weight=3)
        root.grid_columnconfigure(1, weight=1)

        # Hauptbereich
        label_welcome = ctk.CTkLabel(frame_main, text="Willkommen auf der Benutzeroberfläche!", font=("Arial", 24))
        label_welcome.pack(pady=20)
        
        button_projekt_auswahl = ctk.CTkButton(frame_main, text="Projekt auswählen oder erstellen", command=projekt_auswaehlen_oder_erstellen)
        button_projekt_auswahl.pack(pady=10)

        

        # Rechte Spalte für Hinweise und To-Do-Anweisungen
        label_todo_title = ctk.CTkLabel(frame_right, text="Was zu tun ist", font=("Arial", 18))
        label_todo_title.pack(pady=10)

        label_todo_content = ctk.CTkLabel(
            frame_right,
            text="1. Wählen Sie ein Projekt aus oder erstellen Sie ein neues.\n"
                 "2. Nutzen Sie die Menüoptionen zur Projektverwaltung.\n"
                 "3. Öffnen Sie Archicad-Dateien zur weiteren Bearbeitung.",
            font=("Arial", 14),
            justify="left",
            wraplength=280
        )
        label_todo_content.pack(pady=10)

    def projekt_auswaehlen_oder_erstellen():
        option = messagebox.askyesno("Projekt", "Möchten Sie ein bestehendes Projekt öffnen? (Ja) oder ein neues erstellen? (Nein)")
        if option:
            ordner = filedialog.askdirectory(title="Wählen Sie einen bestehenden Projektordner aus")
            if ordner:
                neue_projekt_oberflaeche(ordner)
            else:
                messagebox.showerror("Fehler", "Kein Projektordner ausgewählt.")
        else:
            neues_projekt_erstellen()

    def neues_projekt_erstellen():
        ordner = filedialog.askdirectory(title="Wählen Sie einen Ordner aus, um das neue Projekt zu speichern")
        if ordner:
            # Benutzer nach Projektnamen fragen
            projekt_name = simpledialog.askstring("Projektname", "Bitte geben Sie den Projektnamen ein:")
            if not projekt_name:
                messagebox.showerror("Fehler", "Kein Projektname angegeben.")
                return
            
            # Bestimme die nächste Projektnummer
            projekt_nummer = 1
            while True:
                projekt_ordner_name = f"{projekt_nummer:03d}_{projekt_name}"
                projekt_pfad = os.path.join(ordner, projekt_ordner_name)
                if not os.path.exists(projekt_pfad):
                    os.makedirs(projekt_pfad)  # Erstellt den Projektordner
                    break
                projekt_nummer += 1
            
            # Neue Benutzeroberfläche anzeigen
            neue_projekt_oberflaeche(projekt_pfad)

    def neue_projekt_oberflaeche(ordner):
        for widget in root.winfo_children():
            widget.destroy()
        
        frame_main = ctk.CTkFrame(root)
        frame_main.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        frame_right = ctk.CTkFrame(root, width=200)
        frame_right.grid(row=0, column=1, padx=10, pady=20, sticky="ns")

        root.grid_columnconfigure(0, weight=3)
        root.grid_columnconfigure(1, weight=1)

        # Hauptbereich
        label_projekt = ctk.CTkLabel(frame_main, text=f"Projekt im Ordner: {ordner}", font=("Arial", 16))
        label_projekt.pack(pady=20)

        button_archicad_option = ctk.CTkButton(frame_main, text="Archicad-Optionen", command=lambda: archicad_optionen(ordner))
        button_archicad_option.pack(pady=10)

        button_script_uebersicht = ctk.CTkButton(frame_main, text="Geöffnete VS Code Skripte anzeigen", command=zeige_script_uebersicht)
        button_script_uebersicht.pack(pady=10)

        

        # Rechte Spalte für Hinweise und To-Do-Anweisungen
        label_todo_title = ctk.CTkLabel(frame_right, text="Projektverwaltung", font=("Arial", 18))
        label_todo_title.pack(pady=10)

        label_todo_content = ctk.CTkLabel(
            frame_right,
            text="1. Wählen Sie eine Archicad-Option aus.\n"
                 "2. Nutzen Sie die verfügbaren Tools zur Verwaltung.",
            font=("Arial", 14),
            justify="left"
        )
        label_todo_content.pack(pady=10)

    def archicad_optionen(ordner):
        if archicad_datei_geoeffnet[0]:
            if messagebox.askyesno("Archicad", "Es scheint, dass bereits eine Archicad-Datei geöffnet ist. Möchten Sie trotzdem eine neue Datei öffnen?"):
                archicad_datei_geoeffnet[0] = False  # Setze den Status zurück, um eine neue Datei öffnen zu können
            else:
                return
        
        datei = filedialog.askopenfilename(title="Wählen Sie eine Archicad-Datei aus", initialdir=os.path.expanduser("~"), filetypes=[("Archicad Einzelprojekt (.pln)", "*.pln"), ("Alle Dateien", "*.*")])
        if datei:
            try:
                # Öffnet die Archicad-Datei mit dem Standardprogramm für .pln Dateien
                subprocess.Popen([datei], shell=True)
                archicad_datei_geoeffnet[0] = True  # Setze den Status auf "geöffnet"
                messagebox.showinfo("Datei geöffnet", f"Die Datei '{os.path.basename(datei)}' wurde erfolgreich geöffnet.")
                
                # Schließe das Fenster der Projektverwaltung
                root.destroy()

                # Python-Palette nach Öffnen der Archicad-Datei anzeigen
                zeige_python_palette()
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Öffnen der Datei: {str(e)}")

    def zeige_python_palette():
        # Neues Fenster öffnen, um auf das geöffnete Visual Studio Projekt zuzugreifen
        palette_fenster = ctk.CTkToplevel()
        palette_fenster.title("Python-Palette")
        palette_fenster.geometry("600x400")

        label_info = ctk.CTkLabel(palette_fenster, text="Hier können Sie auf das aktuell geöffnete Visual Studio Projekt zugreifen.", font=("Arial", 14))
        label_info.pack(pady=20)

        # Beispiel: Aktionen zur Integration mit Visual Studio könnten hier hinzugefügt werden
        button_vs_aktion = ctk.CTkButton(palette_fenster, text="Aktion im Visual Studio ausführen", command=lambda: messagebox.showinfo("Info", "Diese Funktion wird bald verfügbar sein."))
        button_vs_aktion.pack(pady=10)

    def zeige_script_uebersicht():
        # Neues Fenster öffnen, um eine Übersicht der geöffneten Skripte anzuzeigen
        uebersicht_fenster = ctk.CTkToplevel()
        uebersicht_fenster.title("Übersicht der geöffneten VS Code Skripte")
        uebersicht_fenster.geometry("600x400")

        label_info = ctk.CTkLabel(uebersicht_fenster, text="Geöffnete Skripte im VS Code:", font=("Arial", 14))
        label_info.pack(pady=20)

        # Hier sollten alle geöffneten Dateien in VS Code angezeigt werden
        # Beispielhafte Liste von Skripten (kann durch tatsächliche Integration mit VS Code erweitert werden)
        geoeffnete_skripte = [
            "main.py",
            "Stützen_Analyse.py",
            "interface_final.py",
            "test_interface.py"
        ]

        for skript in geoeffnete_skripte:
            label_skript = ctk.CTkLabel(uebersicht_fenster, text=skript, font=("Arial", 12))
            label_skript.pack(anchor="w", padx=20)

    # Widgets für Anmeldeoberfläche
    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    frame_right = ctk.CTkFrame(root, width=200)
    frame_right.grid(row=0, column=1, padx=10, pady=20, sticky="ns")

    root.grid_columnconfigure(0, weight=3)
    root.grid_columnconfigure(1, weight=1)

    # Hauptbereich für Anmeldeinformationen
    label_title = ctk.CTkLabel(frame, text="Willkommen zurück!", font=("Arial", 24))
    label_title.pack(pady=12, padx=10)

    label_subtitle = ctk.CTkLabel(frame, text="Melden Sie sich in Ihrem Konto an.", font=("Arial", 14))
    label_subtitle.pack(pady=5, padx=10)

    entry_email = ctk.CTkEntry(frame, placeholder_text="Benutzername")
    entry_email.bind("<Return>", lambda event: entry_password.focus())
    entry_email.pack(pady=12, padx=10)

    entry_password = ctk.CTkEntry(frame, placeholder_text="Passwort", show="*")
    entry_password.pack(pady=12, padx=10)
    entry_password.bind("<Return>", lambda event: login())

    button_login = ctk.CTkButton(frame, text="Anmelden", command=login)
    button_login.pack(pady=12, padx=10)

    # Rechte Spalte für Hinweise und To-Do-Anweisungen
    label_todo_title = ctk.CTkLabel(frame_right, text="Was zu tun ist", font=("Arial", 18))
    label_todo_title.pack(pady=10)

    label_todo_content = ctk.CTkLabel(
        frame_right,
        text="1. Geben Sie Ihren Benutzernamen und Ihr Passwort ein.\n"
             "2. Drücken Sie die Eingabetaste oder klicken Sie auf 'Anmelden'.",
        font=("Arial", 14),
        justify="left"
    )
    label_todo_content.pack(pady=10)

    # Hauptfenster starten
    root.mainloop()

# Nur ausführen, wenn das Skript direkt gestartet wird
if __name__ == "__main__":
    start_app()
