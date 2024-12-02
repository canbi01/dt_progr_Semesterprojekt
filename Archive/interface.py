import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import subprocess

# Hauptfenster erstellen
ctk.set_appearance_mode("Dark")  # Dark mode für modernes Aussehen
ctk.set_default_color_theme("dark-blue")  # Setze ein Farbschema

root = ctk.CTk()
root.title("Anmeldeoberfläche")
root.geometry("600x500")
root.resizable(True, True)  # Fenstergröße anpassbar machen und auf den gesamten Bildschirm vergrößerbar

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
    
    label_welcome = ctk.CTkLabel(root, text="Willkommen auf der neuen Benutzeroberfläche!", font=("Arial", 24))
    label_welcome.pack(pady=20)
    
    button_neues_projekt = ctk.CTkButton(root, text="Neues Projekt erstellen", command=neues_projekt_erstellen)
    button_neues_projekt.pack(pady=10)

def neues_projekt_erstellen():
    ordner = filedialog.askdirectory(title="Wählen Sie einen Ordner aus, um das neue Projekt zu speichern")
    if ordner:
        for widget in root.winfo_children():
            widget.destroy()  # Löscht alle Widgets im Fenster
        label_projekt = ctk.CTkLabel(root, text=f"Neues Projekt erstellt im Ordner: {ordner}", font=("Arial", 16))
        label_projekt.pack(pady=20)

        button_archicad = ctk.CTkButton(root, text="Archicad Datei öffnen", command=archicad_datei_oeffnen)
        button_archicad.pack(pady=10)

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
frame.pack(pady=40, padx=20, fill="both", expand=True)

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

# Hauptfenster starten
root.mainloop()
