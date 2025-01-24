import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, Listbox
import json
import os

# File to store projects
projects_file = "projects.json"

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

# Add "AEP" logo at the top right of each window
def add_aep_logo(window):
    logo_label = tk.Label(window, text="AEP", font=("Arial", 20, "bold"), fg="white")
    logo_label.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

def start_license_verification():
    """Startet die Lizenzprüfung."""
    root = tk.Tk()
    root.title("Lizenzprüfung")
    root.geometry("400x200")

    add_aep_logo(root)

    license_key_var = tk.StringVar()

    def verify_license():
        license_key = license_key_var.get()
        if license_key == "123456":
            root.destroy()
        else:
            messagebox.showerror("Fehler", "Ungültige Lizenznummer.")

    tk.Label(root, text="Bitte geben Sie Ihre Lizenznummer ein:", font=("Arial", 14)).pack(pady=10)
    tk.Entry(root, textvariable=license_key_var, font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Prüfen", command=verify_license).pack(pady=10)

    root.mainloop()
    return license_key_var.get()

def select_project_interface():
    root = tk.Tk()
    root.title("AEP - Archicad Efficiency Program")
    root.geometry("800x600")

    add_aep_logo(root)

    projects = load_projects()
    selected_project = tk.StringVar()
    current_project = None

    # Save current project details
    def save_current_project():
        if current_project:
            projects[current_project]["details"]["Parzelle"] = entry_parzelle.get()
            projects[current_project]["details"]["Adresse"] = entry_adresse.get()
            projects[current_project]["details"]["Projektverfasser"] = entry_projektverfasser.get()
            projects[current_project]["details"]["Bauherrschaft"] = entry_bauherrschaft.get()
            projects[current_project]["details"]["Ostausrichtung"] = entry_ost.get()
            projects[current_project]["details"]["Nordausrichtung"] = entry_nord.get()
            projects[current_project]["details"]["Höhe"] = entry_hoehe.get()
            projects[current_project]["details"]["Nordwinkel"] = entry_nordwinkel.get()
            save_projects(projects)
            messagebox.showinfo("Speichern", f"Änderungen für Projekt '{current_project}' wurden gespeichert.")

    # Delete selected project
    def delete_selected_project():
        """Löscht das ausgewählte Projekt aus der Liste und aus dem JSON-File."""
        selection = project_listbox.curselection()
        if not selection:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus, das gelöscht werden soll.")
            return

        selected_project = project_listbox.get(selection)
        if messagebox.askyesno("Projekt löschen", f"Möchten Sie das Projekt '{selected_project}' wirklich löschen?"):
            del projects[selected_project]
            save_projects(projects)
            project_listbox.delete(selection)
            messagebox.showinfo("Gelöscht", f"Projekt '{selected_project}' wurde gelöscht.")
            # Reset the details fields
            entry_parzelle.delete(0, tk.END)
            entry_adresse.delete(0, tk.END)
            entry_projektverfasser.delete(0, tk.END)
            entry_bauherrschaft.delete(0, tk.END)
            entry_ost.delete(0, tk.END)
            entry_nord.delete(0, tk.END)
            entry_hoehe.delete(0, tk.END)
            entry_nordwinkel.delete(0, tk.END)

    # Proceed to shortcut selection
    def proceed_to_shortcut_selection():
        if current_project:
            root.destroy()  # Close the current window
            messagebox.showinfo("Weiterleitung", f"Weiter zur Shortcut-Auswahl für Projekt '{current_project}'...")
            selected_project.set(current_project)

    # Load project details into the fields
    def load_project_details(event):
        nonlocal current_project
        selection = project_listbox.curselection()
        if not selection:
            return
        current_project = project_listbox.get(selection)
        project_details = projects.get(current_project, {}).get("details", {})
        entry_parzelle.delete(0, tk.END)
        entry_parzelle.insert(0, project_details.get("Parzelle", ""))
        entry_adresse.delete(0, tk.END)
        entry_adresse.insert(0, project_details.get("Adresse", ""))
        entry_projektverfasser.delete(0, tk.END)
        entry_projektverfasser.insert(0, project_details.get("Projektverfasser", ""))
        entry_bauherrschaft.delete(0, tk.END)
        entry_bauherrschaft.insert(0, project_details.get("Bauherrschaft", ""))
        entry_ost.delete(0, tk.END)
        entry_ost.insert(0, project_details.get("Ostausrichtung", ""))
        entry_nord.delete(0, tk.END)
        entry_nord.insert(0, project_details.get("Nordausrichtung", ""))
        entry_hoehe.delete(0, tk.END)
        entry_hoehe.insert(0, project_details.get("Höhe", ""))
        entry_nordwinkel.delete(0, tk.END)
        entry_nordwinkel.insert(0, project_details.get("Nordwinkel", ""))

    # Create a new project
    def create_new_project():
        new_project_name = simpledialog.askstring("Neues Projekt", "Projektname eingeben:")
        if new_project_name:
            projects[new_project_name] = {
                "details": {
                    "Parzelle": "",
                    "Adresse": "",
                    "Projektverfasser": "",
                    "Bauherrschaft": "",
                    "Ostausrichtung": "",
                    "Nordausrichtung": "",
                    "Höhe": "",
                    "Nordwinkel": "",
                }
            }
            save_projects(projects)
            project_listbox.insert(tk.END, new_project_name)

    # Left-side project list
    frame_left = tk.Frame(root, width=200, padx=10, pady=10)
    frame_left.pack(side=tk.LEFT, fill=tk.Y)

    project_listbox = Listbox(frame_left, height=25)
    project_listbox.pack(fill=tk.BOTH, expand=True)
    for project in projects.keys():
        project_listbox.insert(tk.END, project)
    project_listbox.bind("<<ListboxSelect>>", load_project_details)

    btn_new_project = tk.Button(frame_left, text="Neues Projekt", command=create_new_project)
    btn_new_project.pack(pady=10)

    # Right-side project details
    frame_right = tk.Frame(root, padx=10, pady=10)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    tk.Label(frame_right, text="Projekt-Infos", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_right, text="Parzelle:").grid(row=1, column=0, sticky=tk.W)
    entry_parzelle = tk.Entry(frame_right, width=50)
    entry_parzelle.grid(row=1, column=1)

    tk.Label(frame_right, text="Adresse:").grid(row=2, column=0, sticky=tk.W)
    entry_adresse = tk.Entry(frame_right, width=50)
    entry_adresse.grid(row=2, column=1)

    tk.Label(frame_right, text="Projektverfasser:").grid(row=3, column=0, sticky=tk.W)
    entry_projektverfasser = tk.Entry(frame_right, width=50)
    entry_projektverfasser.grid(row=3, column=1)

    tk.Label(frame_right, text="Bauherrschaft:").grid(row=4, column=0, sticky=tk.W)
    entry_bauherrschaft = tk.Entry(frame_right, width=50)
    entry_bauherrschaft.grid(row=4, column=1)

    tk.Label(frame_right, text="Ostausrichtung:").grid(row=5, column=0, sticky=tk.W)
    entry_ost = tk.Entry(frame_right, width=50)
    entry_ost.grid(row=5, column=1)

    tk.Label(frame_right, text="Nordausrichtung:").grid(row=6, column=0, sticky=tk.W)
    entry_nord = tk.Entry(frame_right, width=50)
    entry_nord.grid(row=6, column=1)

    tk.Label(frame_right, text="Höhe:").grid(row=7, column=0, sticky=tk.W)
    entry_hoehe = tk.Entry(frame_right, width=50)
    entry_hoehe.grid(row=7, column=1)

    tk.Label(frame_right, text="Nordwinkel:").grid(row=8, column=0, sticky=tk.W)
    entry_nordwinkel = tk.Entry(frame_right, width=50)
    entry_nordwinkel.grid(row=8, column=1)

    btn_save_project = tk.Button(frame_right, text="Speichern", command=save_current_project)
    btn_save_project.grid(row=9, column=0, columnspan=2, pady=10)

    btn_proceed = tk.Button(frame_right, text="Weiter", command=proceed_to_shortcut_selection)
    btn_proceed.grid(row=10, column=0, columnspan=2, pady=10)

    root.mainloop()

<<<<<<< HEAD
    return projects.get(selected_project.get(), None)
=======
    return {"name": current_project, "details": projects.get(current_project, {}).get("details", {})}
>>>>>>> parent of 81c6503 (löschfunktion eingebaut)

def select_shortcut():
    """Zeigt ein Fenster zur Auswahl eines Shortcuts."""
    root = tk.Tk()
    root.title("Shortcut auswählen")
<<<<<<< HEAD
    root.geometry("400x300")
=======
    root.geometry("400x600")

    add_aep_logo(root)
>>>>>>> parent of 81c6503 (löschfunktion eingebaut)

    selected_shortcut = tk.StringVar(value="")

    def confirm_selection():
        if shortcut_listbox.curselection():
            selected_shortcut.set(shortcut_listbox.get(shortcut_listbox.curselection()))
            root.destroy()
        else:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Shortcut aus.")

    tk.Label(root, text="Wählen Sie einen Shortcut aus:", font=("Arial", 14)).pack(pady=10)

    shortcuts = ["Ausmass Baugespann", "Andere Funktion (zukünftig)"]
    shortcut_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    for shortcut in shortcuts:
        shortcut_listbox.insert(tk.END, shortcut)
    shortcut_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    tk.Button(root, text="Weiter", command=confirm_selection).pack(pady=10)

    root.mainloop()
    return selected_shortcut.get()

<<<<<<< HEAD
def show_error(message):
    """Zeigt eine Fehlermeldung in einem Popup-Fenster an."""
    messagebox.showerror("Fehler", message)

def select_output_directory():
    """Startet die Auswahl eines Zielverzeichnisses."""
    return filedialog.askdirectory(title="Zielverzeichnis wählen")

=======
>>>>>>> parent of 81c6503 (löschfunktion eingebaut)
def show_analysis_instructions(project_name):
    """Zeigt Anweisungen zur Analyse an."""
    root = tk.Tk()
    root.title("Anweisungen")
    root.geometry("400x300")

<<<<<<< HEAD
=======
    add_aep_logo(root)

>>>>>>> parent of 81c6503 (löschfunktion eingebaut)
    instructions = (
        f"Öffnen Sie die Archicad-Datei für Projekt {project_name} und folgen Sie diesen Anweisungen:\n\n"
        "1. Navigieren Sie ins 3D-Fenster.\n"
        "2. Öffnen Sie das Stützenwerkzeug und setzen Sie die Element-ID 'Baugespann'.\n"
        "3. Platzieren Sie die Stützen an den gewünschten Stellen."
    )

    tk.Label(root, text=instructions, wraplength=380, justify="left", font=("Arial", 12)).pack(pady=10)

    tk.Button(root, text="Weiter", command=root.destroy).pack(pady=10)

<<<<<<< HEAD
    root.mainloop()
=======
    root.mainloop()

def select_output_directory():
    """Startet die Auswahl eines Zielverzeichnisses."""
    return filedialog.askdirectory(title="Zielverzeichnis wählen")
>>>>>>> parent of 81c6503 (löschfunktion eingebaut)
