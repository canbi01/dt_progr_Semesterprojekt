import customtkinter as ctk
from tkinter import messagebox, filedialog
import os

# Globale Variablen für Vermessungspunkt-Offsets
SURVEY_POINT_OFFSET_X = 0.0
SURVEY_POINT_OFFSET_Y = 0.0
SURVEY_POINT_OFFSET_Z = 0.0
output_directory = ""

# Funktion zum Speichern der Offsets in einer Datei
def save_offsets():
    global SURVEY_POINT_OFFSET_X, SURVEY_POINT_OFFSET_Y, SURVEY_POINT_OFFSET_Z
    try:
        file_path = "survey_offsets.txt"
        with open(file_path, "w") as file:
            file.write(f"SURVEY_POINT_OFFSET_X={SURVEY_POINT_OFFSET_X}\n")
            file.write(f"SURVEY_POINT_OFFSET_Y={SURVEY_POINT_OFFSET_Y}\n")
            file.write(f"SURVEY_POINT_OFFSET_Z={SURVEY_POINT_OFFSET_Z}\n")
        messagebox.showinfo("Erfolg", f"Offsets erfolgreich in {file_path} gespeichert!")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Speichern der Offsets: {e}")

# Hauptfenster erstellen
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Archicad Baugespann-Auswertung")
root.geometry("600x400")

# Schrittweises Navigationssystem
current_step = 1

# Funktionen für die Schritte

def show_next_step():
    global current_step
    if current_step == 1:
        show_step_open_file()
    elif current_step == 2:
        show_step_enter_offsets()
    elif current_step == 3:
        show_step_select_output()
    elif current_step == 4:
        root.destroy()  # Beendet das GUI, um das Analyse-Skript auszuführen

# Schritt 1: Anmelden

def show_step_login():
    clear_window()

    label_title = ctk.CTkLabel(root, text="Anmelden", font=("Arial", 24))
    label_title.pack(pady=12, padx=10)

    label_subtitle = ctk.CTkLabel(root, text="Melden Sie sich an, um fortzufahren.", font=("Arial", 14))
    label_subtitle.pack(pady=5, padx=10)

    entry_email = ctk.CTkEntry(root, placeholder_text="Benutzername")
    entry_email.pack(pady=12, padx=10)

    entry_password = ctk.CTkEntry(root, placeholder_text="Passwort", show="*")
    entry_password.pack(pady=12, padx=10)

    def login():
        benutzername = entry_email.get()
        passwort = entry_password.get()
        if benutzername == "admin" and passwort == "123":
            global current_step
            current_step += 1
            show_next_step()
        else:
            messagebox.showerror("Fehler", "Falscher Benutzername oder falsches Passwort")

    button_login = ctk.CTkButton(root, text="Anmelden", command=login)
    button_login.pack(pady=12, padx=10)

# Schritt 2: Archicad-Datei öffnen

def show_step_open_file():
    clear_window()

    label_instructions = ctk.CTkLabel(root, text="Öffnen Sie die gewünschte Archicad-Datei.", font=("Arial", 14), justify="left", wraplength=550)
    label_instructions.pack(pady=10)

    def continue_to_next():
        global current_step
        current_step += 1
        show_next_step()

    button_continue = ctk.CTkButton(root, text="Weiter", command=continue_to_next)
    button_continue.pack(pady=10)

# Schritt 3: Offsets eingeben

def show_step_enter_offsets():
    clear_window()

    label_instructions = ctk.CTkLabel(root, text=(
        "Gehen Sie über das Menu > Verwaltung > Projekteinstellung > Lageeinstellungen und kopieren Sie die Vermessungspunkt-Koordinaten in die Felder."
    ), font=("Arial", 14), justify="left", wraplength=550)
    label_instructions.pack(pady=10)

    frame_inputs = ctk.CTkFrame(root)
    frame_inputs.pack(pady=10, padx=10, fill="both", expand=True)

    label_x = ctk.CTkLabel(frame_inputs, text="Nordausrichtung:")
    label_x.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_x = ctk.CTkEntry(frame_inputs)
    entry_x.grid(row=0, column=1, padx=5, pady=5)

    label_y = ctk.CTkLabel(frame_inputs, text="Ostausrichtung:")
    label_y.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_y = ctk.CTkEntry(frame_inputs)
    entry_y.grid(row=1, column=1, padx=5, pady=5)

    label_z = ctk.CTkLabel(frame_inputs, text="Höhe:")
    label_z.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_z = ctk.CTkEntry(frame_inputs)
    entry_z.grid(row=2, column=1, padx=5, pady=5)

    def save_and_continue():
        global SURVEY_POINT_OFFSET_X, SURVEY_POINT_OFFSET_Y, SURVEY_POINT_OFFSET_Z
        try:
            SURVEY_POINT_OFFSET_X = float(entry_x.get())
            SURVEY_POINT_OFFSET_Y = float(entry_y.get())
            SURVEY_POINT_OFFSET_Z = float(entry_z.get())
            save_offsets()
            global current_step
            current_step += 1
            show_next_step()
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie gültige numerische Werte ein.")

    button_save_continue = ctk.CTkButton(root, text="Speichern und Weiter", command=save_and_continue)
    button_save_continue.pack(pady=10)

# Schritt 4: Speicherpfad auswählen

def show_step_select_output():
    clear_window()

    label_instructions = ctk.CTkLabel(root, text="Wählen Sie ein Zielverzeichnis für die Ergebnisse der Analyse.", font=("Arial", 14), justify="left", wraplength=550)
    label_instructions.pack(pady=10)

    def select_directory():
        global output_directory
        output_directory = filedialog.askdirectory(title="Zielverzeichnis wählen")
        if output_directory:
            messagebox.showinfo("Verzeichnis gewählt", f"Dateien werden in {output_directory} gespeichert.")

    def start_analysis():
        if output_directory:
            global current_step
            current_step += 1
            show_next_step()
        else:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Zielverzeichnis aus.")

    button_select_directory = ctk.CTkButton(root, text="Verzeichnis wählen", command=select_directory)
    button_select_directory.pack(pady=10)

    button_start_analysis = ctk.CTkButton(root, text="Analyse starten", command=start_analysis)
    button_start_analysis.pack(pady=10)

# Hilfsfunktion zum Löschen aller Widgets im Fenster
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Starte mit Schritt 1
show_step_login()

# Hauptfenster starten
root.mainloop()

