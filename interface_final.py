import customtkinter as ctk
from tkinter import messagebox, filedialog, simpledialog
import os
import subprocess

# Funktionen und GUI

def start_app():
    # Hauptfenster erstellen
    ctk.set_appearance_mode("Dark")  # Dark mode für modernes Aussehen
    ctk.set_default_color_theme("dark-blue")  # Setze ein Farbschema

    root = ctk.CTk()
    root.title("Anmeldeoberfläche")
    root.geometry("1200x700")  # Breiteres Fenster für zusätzliche Spalte
    root.resizable(True, True)  # Fenstergröße anpassbar machen

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
        label_welcome = ctk.CTkLabel(frame_main, text="Willkommen auf der neuen Benutzeroberfläche!", font=("Arial", 24))
        label_welcome.pack(pady=20)
        
        button_neues_projekt = ctk.CTkButton(frame_main, text="Neues Projekt erstellen", command=neues_projekt_erstellen)
        button_neues_projekt.pack(pady=10)

        # Rechte Spalte für Hinweise und To-Do-Anweisungen
        label_todo_title = ctk.CTkLabel(frame_right, text="Was zu tun ist", font=("Arial", 18))
        label_todo_title.pack(pady=10)

        label_todo_content = ctk.CTkLabel(
            frame_right,
            text="1. Melden Sie sich an, um fortzufahren.\n"
                 "2. Klicken Sie auf 'Neues Projekt erstellen', um ein neues Projekt zu starten.\n"
                 "3. Wählen Sie den Speicherort für das neue Projekt.\n"
                 "4. Öffnen Sie Archicad-Dateien zur weiteren Bearbeitung.",
            font=("Arial", 14),
            justify="left",
            wraplength=280
        )
        label_todo_content.pack(pady=10)

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
        frame_main = ctk.CTkFrame(root)
        frame_main.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        frame_right = ctk.CTkFrame(root, width=200)
        frame_right.grid(row=0, column=1, padx=10, pady=20, sticky="ns")

        root.grid_columnconfigure(0, weight=3)
        root.grid_columnconfigure(1, weight=1)

        # Hauptbereich
        label_projekt = ctk.CTkLabel(frame_main, text=f"Neues Projekt erstellt im Ordner: {ordner}", font=("Arial", 16))
        label_projekt.pack(pady=20)

        button_archicad = ctk.CTkButton(frame_main, text="Archicad Datei öffnen", command=archicad_datei_oeffnen)
        button_archicad.pack(pady=10)

        # Rechte Spalte für Hinweise und To-Do-Anweisungen
        label_todo_title = ctk.CTkLabel(frame_right, text="Was zu tun ist", font=("Arial", 18))
        label_todo_title.pack(pady=10)

        label_todo_content = ctk.CTkLabel(
            frame_right,
            text="1. Wählen Sie eine Archicad-Datei aus, um sie zu bearbeiten.\n"
                 "2. Nutzen Sie die Optionen im Menü, um das Projekt zu verwalten.",
            font=("Arial", 14),
            justify="left"
        )
        label_todo_content.pack(pady=10)

    def archicad_datei_oeffnen():
        datei = filedialog.askopenfilename(title="Wählen Sie eine Archicad-Datei aus", initialdir=os.path.expanduser("~"), filetypes=[("Archicad Einzelprojekt (.pln)", "*.pln"), ("Alle Dateien", "*.*")])
        if datei:
            try:
                # Öffnet die Archicad-Datei mit dem Standardprogramm für .pln Dateien
                subprocess.Popen([datei], shell=True)
                messagebox.showinfo("Datei geöffnet", f"Die Datei '{os.path.basename(datei)}' wurde erfolgreich geöffnet.")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Öffnen der Datei: {str(e)}")

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
