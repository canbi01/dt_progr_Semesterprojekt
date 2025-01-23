import customtkinter as ctk
import json
from tkinter import messagebox, filedialog
import os

# Globale Variablen
projects_file = "projects.json"
current_project = None

# Lade gespeicherte Projekte
def load_projects():
    if os.path.exists(projects_file):
        with open(projects_file, "r") as file:
            return json.load(file)
    return {}

# Speichere Projekte
def save_projects(projects):
    with open(projects_file, "w") as file:
        json.dump(projects, file, indent=4)

def main_interface():
    global current_project
    projects = load_projects()

    def verify_license():
        license_key = entry_license.get()
        if license_key == "123456":
            project_selection()
        else:
            messagebox.showerror("Ungültige Lizenz", "Bitte geben Sie eine gültige Lizenznummer ein.")

    def project_selection():
        nonlocal projects
        root.destroy()
        project_window = ctk.CTk()
        project_window.title("Projekt auswählen")

        def on_project_select():
            nonlocal current_project
            selected_project = project_listbox.get(project_listbox.curselection())
            current_project = projects[selected_project]
            project_window.destroy()

        def add_project():
            def save_new_project():
                new_project = {
                    "name": entry_project_name.get(),
                    "details": {
                        "Parzelle": entry_parzelle.get(),
                        "Adresse": entry_adresse.get(),
                        "Büro": entry_buero.get(),
                        "Büro-Adresse": entry_buero_adresse.get(),
                        "Bauherrschaft": {
                            "Name": entry_bauherr_name.get(),
                            "Adresse": entry_bauherr_adresse.get(),
                        },
                    },
                    "offsets": {
                        "Ostausrichtung": float(entry_ost.get()),
                        "Nordausrichtung": float(entry_nord.get()),
                        "Höhe": float(entry_hoehe.get()),
                        "Nordwinkel": float(entry_nordwinkel.get()),
                    },
                }
                projects[new_project["name"]] = new_project
                save_projects(projects)
                add_project_window.destroy()
                project_selection()

            add_project_window = ctk.CTkToplevel(project_window)
            add_project_window.title("Neues Projekt erfassen")
            
            # GUI für Projekteingabe (Name, Details, Offsets)
            entry_project_name = ctk.CTkEntry(add_project_window, placeholder_text="Projektname")
            entry_parzelle = ctk.CTkEntry(add_project_window, placeholder_text="Parzelle")
            entry_adresse = ctk.CTkEntry(add_project_window, placeholder_text="Adresse")
            entry_buero = ctk.CTkEntry(add_project_window, placeholder_text="Büro")
            entry_buero_adresse = ctk.CTkEntry(add_project_window, placeholder_text="Büro-Adresse")
            entry_bauherr_name = ctk.CTkEntry(add_project_window, placeholder_text="Bauherrschaft Name")
            entry_bauherr_adresse = ctk.CTkEntry(add_project_window, placeholder_text="Bauherrschaft Adresse")
            entry_ost = ctk.CTkEntry(add_project_window, placeholder_text="Ostausrichtung")
            entry_nord = ctk.CTkEntry(add_project_window, placeholder_text="Nordausrichtung")
            entry_hoehe = ctk.CTkEntry(add_project_window, placeholder_text="Höhe")
            entry_nordwinkel = ctk.CTkEntry(add_project_window, placeholder_text="Nordwinkel")

            # Speichern-Button
            button_save = ctk.CTkButton(add_project_window, text="Speichern", command=save_new_project)
            button_save.pack()

        project_listbox = ctk.CTkListbox(project_window)
        for project_name in projects.keys():
            project_listbox.insert("end", project_name)

        project_listbox.pack()
        ctk.CTkButton(project_window, text="Projekt auswählen", command=on_project_select).pack()
        ctk.CTkButton(project_window, text="Neues Projekt hinzufügen", command=add_project).pack()
        project_window.mainloop()

    # Login-Bildschirm
    root = ctk.CTk()
    root.title("AEP-ArchicadEfficiencyProgramm")
    label_title = ctk.CTkLabel(root, text="Bitte tragen Sie Ihre Lizenznummer ein")
    label_title.pack()

    entry_license = ctk.CTkEntry(root, placeholder_text="Lizenznummer")
    entry_license.pack()

    button_verify = ctk.CTkButton(root, text="Weiter", command=verify_license)
    button_verify.pack()

    root.mainloop()
    return "123456", current_project
