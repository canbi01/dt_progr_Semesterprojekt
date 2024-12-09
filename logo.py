import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Bild laden
bild_pfad = 'C:\\Users\\Ben Wild\\OneDrive - Hochschule Luzern\\00_MO3_Programmieren\\dt_progr_Semesterarbeit\\Logo_Architekten.png'
bild = Image.open(bild_pfad)

# In NumPy-Array konvertieren und als uint8 speichern
bild_array = np.array(bild, dtype=np.uint8)
np.save('bild.npy', bild_array)
print("Das Bild wurde als bild.npy gespeichert.")

# Datei laden
bild = np.load('bild.npy', allow_pickle=False)  # Sicherstellen, dass es kein Object-Array ist

# Datentyp und Form prüfen
print(f"Datentyp: {bild.dtype}, Form: {bild.shape}")

# Bild anzeigen
plt.imshow(bild)
plt.axis('off')
plt.show()
