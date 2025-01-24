import customtkinter as ctk
from tkinter import messagebox, filedialog, Listbox, Canvas
import json
import os

# File to store projects
projects_file = "projects.json"

# Set global theme for CustomTkinter
ctk.set_appearance_mode("Dark")  # Options: "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Modern blue-based theme

# Load projects from file
def load_projects():
    if os.path.exists(projects_file):
        with open(projects_file, "r") as file:
            return json.load(file)
    return {}

# Save projects to file
def save_projects(projects):
    with open(projects_file, "w") as file:
        json.dump(projects, file, indent=4)

# License verification with splash screen animation
def start_license_verification():
    license_key = show_login_window()
    print(f"License Key from Login Window: {license_key}")  # Debugging Output
    return license_key

# Show login window for license verification
def show_login_window():
    root = ctk.CTk()
    root.title("AEP - ArchicadEfficiencyProgramm")
    root.geometry("500x300")

    # Variable to store the license key
    license_key_var = ctk.StringVar(value="")

    def verify_license():
        entered_key = entry_license.get()
        print(f"Entered License Key: {entered_key}")  # Debugging Output
        if entered_key == "123456":
            license_key_var.set(entered_key)  # Set the license key
            root.destroy()  # Close the window
        else:
            messagebox.showerror("Fehler", "Ungültige Lizenznummer.")

    label_title = ctk.CTkLabel(root, text="Willkommen Zurück!", font=("Roboto", 24))
    label_title.pack(pady=20)

    label_subtitle = ctk.CTkLabel(root, text="Bitte tragen Sie Ihre Lizenznummer ein.", font=("Roboto", 16))
    label_subtitle.pack(pady=10)

    entry_license = ctk.CTkEntry(root, placeholder_text="Lizenznummer", width=300, height=40)
    entry_license.pack(pady=20)

    button_verify = ctk.CTkButton(root, text="Weiter", command=verify_license, corner_radius=10)
    button_verify.pack(pady=20)

    root.mainloop()
    # Return the value after the window is closed
    return license_key_var.get()

# Project selection
def select_project():
    projects = load_projects()

    def on_project_select():
        nonlocal current_project
        try:
            selected_project = project_listbox.get(project_listbox.curselection())
            current_project = projects.get(selected_project, None)
            project_window.destroy()
        except Exception:
            messagebox.showerror("Fehler", "Bitte ein Projekt auswählen.")

    def add_project():
        try:
            new_project = {
                "name": entry_project_name.get(),
                "details": {
                    "Parzelle": entry_parzelle.get(),
                    "Adresse": entry_adresse.get(),
                    "Büro": entry_buero.get(),
                    "Büro-Adresse": entry_buero_adresse.get(),
                    "Bauherrschaft": {
                        "Name": entry_bauherr_name.get(),
                        "Adresse": entry_bauherr_adresse.get()
                    },
                    "offsets": {
                        "Ostausrichtung": float(entry_ost.get()),
                        "Nordausrichtung": float(entry_nord.get()),
                        "Höhe": float(entry_hoehe.get()),
                        "Nordwinkel": float(entry_nordwinkel.get())
                    }
                }
            }
            projects[new_project["name"]] = new_project
            save_projects(projects)
            project_listbox.insert("end", new_project["name"])
        except ValueError:
            messagebox.showerror("Fehler", "Bitte alle Felder korrekt ausfüllen.")

    current_project = None
    project_window = ctk.CTk()
    project_window.title("Projekte")
    project_window.geometry("600x500")

    label_projects = ctk.CTkLabel(project_window, text="Wählen Sie ein Projekt aus oder erstellen Sie ein Neues.", font=("Roboto", 18))
    label_projects.pack(pady=20)

    project_listbox = Listbox(project_window, bg="#1E1E2E", fg="#FFFFFF", highlightbackground="#4CAF50", font=("Roboto", 12), width=50, height=10)
    for project in projects.keys():
        project_listbox.insert("end", project)
    project_listbox.pack(pady=20)

    button_select = ctk.CTkButton(project_window, text="Projekt auswählen", command=on_project_select, corner_radius=10)
    button_select.pack(pady=10)

    frame_add_project = ctk.CTkFrame(project_window)
    frame_add_project.pack(pady=20, padx=20)

    label_add_project = ctk.CTkLabel(frame_add_project, text="Neues Projekt erstellen", font=("Roboto", 16))
    label_add_project.pack(pady=10)

    entry_project_name = ctk.CTkEntry(frame_add_project, placeholder_text="Projektname", width=300)
    entry_project_name.pack(pady=5)
    entry_parzelle = ctk.CTkEntry(frame_add_project, placeholder_text="Parzelle", width=300)
    entry_parzelle.pack(pady=5)
    entry_adresse = ctk.CTkEntry(frame_add_project, placeholder_text="Adresse", width=300)
    entry_adresse.pack(pady=5)
    entry_buero = ctk.CTkEntry(frame_add_project, placeholder_text="Büro", width=300)
    entry_buero.pack(pady=5)
    entry_buero_adresse = ctk.CTkEntry(frame_add_project, placeholder_text="Büro-Adresse", width=300)
    entry_buero_adresse.pack(pady=5)
    entry_bauherr_name = ctk.CTkEntry(frame_add_project, placeholder_text="Bauherr Name", width=300)
    entry_bauherr_name.pack(pady=5)
    entry_bauherr_adresse = ctk.CTkEntry(frame_add_project, placeholder_text="Bauherr Adresse", width=300)
    entry_bauherr_adresse.pack(pady=5)

    entry_ost = ctk.CTkEntry(frame_add_project, placeholder_text="Ostausrichtung", width=300)
    entry_ost.pack(pady=5)
    entry_nord = ctk.CTkEntry(frame_add_project, placeholder_text="Nordausrichtung", width=300)
    entry_nord.pack(pady=5)
    entry_hoehe = ctk.CTkEntry(frame_add_project, placeholder_text="Höhe", width=300)
    entry_hoehe.pack(pady=5)
    entry_nordwinkel = ctk.CTkEntry(frame_add_project, placeholder_text="Nordwinkel", width=300)
    entry_nordwinkel.pack(pady=5)

    button_add_project = ctk.CTkButton(frame_add_project, text="Projekt hinzufügen", command=add_project, corner_radius=10)
    button_add_project.pack(pady=10)

    project_window.mainloop()

    return current_project

# Select a shortcut
def select_shortcut():
    shortcuts = ["Ausmass Baugespann", "...coming soon..."]
    selected_shortcut = None

    def on_select():
        nonlocal selected_shortcut
        try:
            selected_shortcut = shortcut_listbox.get(shortcut_listbox.curselection())
            shortcut_window.destroy()
        except Exception:
            messagebox.showerror("Fehler", "Bitte einen Shortcut auswählen.")

    shortcut_window = ctk.CTk()
    shortcut_window.title("Shortcut auswählen")
    shortcut_window.geometry("400x300")

    label_shortcuts = ctk.CTkLabel(shortcut_window, text="Wählen Sie einen AEP-Shortcut aus.", font=("Roboto", 16))
    label_shortcuts.pack(pady=20)

    shortcut_listbox = Listbox(shortcut_window, bg="#1E1E2E", fg="#FFFFFF", highlightbackground="#4CAF50", font=("Roboto", 12), width=40, height=5)
    for shortcut in shortcuts:
        shortcut_listbox.insert("end", shortcut)
    shortcut_listbox.pack(pady=20)

    button_select = ctk.CTkButton(shortcut_window, text="Weiter", command=on_select, corner_radius=10)
    button_select.pack(pady=20)

    shortcut_window.mainloop()

    return selected_shortcut

# Error display
def show_error(message):
    messagebox.showerror("Fehler", message)

# Instructions display
def show_analysis_instructions(project_name):
    instruction_window = ctk.CTk()
    instruction_window.title("Anweisungen")
    instruction_window.geometry("500x400")

    label_instructions = ctk.CTkLabel(
        instruction_window,
        text=(
            f"Öffnen Sie die Archicad-Datei für Projekt {project_name} und folgen Sie diesen Anweisungen:\n\n"
            "1. Navigieren Sie ins 3D-Fenster.\n"
            "2. Öffnen Sie das Stützenwerkzeug und setzen Sie die Element-ID 'Baugespann'.\n"
            "3. Platzieren Sie die Stützen an den gewünschten Stellen."
        ),
        font=("Roboto", 16),
        justify="left",
        wraplength=450
    )
    label_instructions.pack(pady=20)

    button_continue = ctk.CTkButton(instruction_window, text="Weiter", command=instruction_window.destroy, corner_radius=10)
    button_continue.pack(pady=20)

    instruction_window.mainloop()

# Output directory selection
def select_output_directory():
    return filedialog.askdirectory(title="Zielverzeichnis wählen")
