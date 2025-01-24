import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os

# Globale Variablen
output_directory = ""
current_project = None
projects_file = "projects.json"

# Projekte speichern/laden
def save_projects(projects):
    with open(projects_file, "w") as file:
        json.dump(projects, file)

def load_projects():
    if not os.path.exists(projects_file):
        return {}
    with open(projects_file, "r") as file:
        return json.load(file)

def main_interface():
    global output_directory, current_project
    projects = load_projects()

    # Interface Logik
    def show_projects():
        for widget in root.winfo_children():
            widget.destroy()

        # Projektliste anzeigen
        for key, project in projects.items():
            btn = ctk.CTkButton(root, text=project["Projekt"], command=lambda k=key: select_project(k))
            btn.pack(pady=5)

        # Neues Projekt erfassen
        new_project_btn = ctk.CTkButton(root, text="+ Neues Projekt erfassen", command=create_new_project)
        new_project_btn.pack(pady=10)

    def select_project(key):
        global current_project
        current_project = projects[key]

        # Projektdetails anzeigen
        show_project_details(key)

    def show_project_details(key):
        for widget in root.winfo_children():
            widget.destroy()

        project = projects[key]

        for field, value in project.items():
            label = ctk.CTkLabel(root, text=f"{field}: {value}")
            label.pack()

        # Weiter- und Zurück-Buttons
        ctk.CTkButton(root, text="Weiter", command=select_output_directory).pack(pady=10)
        ctk.CTkButton(root, text="Zurück", command=show_projects).pack(pady=5)

    def select_output_directory():
        global output_directory
        output_directory = filedialog.askdirectory(title="Zielverzeichnis wählen")
        if output_directory:
            root.destroy()

    def create_new_project():
        new_project_window = ctk.CTkToplevel()
        new_project_window.title("Neues Projekt erfassen")

        # Eingabefelder für Projektdaten
        entries = {}
        fields = ["Projekt", "Adresse", "Planummer", "Bauherrschaft", "Adresse_Bauherrschaft"]
        for field in fields:
            label = ctk.CTkLabel(new_project_window, text=field)
            label.pack()
            entry = ctk.CTkEntry(new_project_window)
            entry.pack()
            entries[field] = entry

        def save_new_project():
            key = entries["Projekt"].get()
            projects[key] = {field: entry.get() for field, entry in entries.items()}
            projects[key]["Georeferenzierung"] = {
                "SURVEY_POINT_OFFSET_X": 0.0,
                "SURVEY_POINT_OFFSET_Y": 0.0,
                "SURVEY_POINT_OFFSET_Z": 0.0,
                "SURVEY_NORDWINKELOFFSET": 0.0,
            }
            save_projects(projects)
            new_project_window.destroy()
            show_projects()

        ctk.CTkButton(new_project_window, text="Speichern", command=save_new_project).pack()

    root = ctk.CTk()
    root.title("AEP-ArchicadEfficiencyProgramm")
    root.geometry("600x400")
    show_projects()
    root.mainloop()

    return current_project, output_directory
