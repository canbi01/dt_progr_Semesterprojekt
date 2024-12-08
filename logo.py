import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Bild laden
bild_pfad = 'C:\\Users\\Ben Wild\\OneDrive - Hochschule Luzern\\00_MO3_Programmieren\\dt_progr_Semesterarbeit\\Logo_Architekten.png'
bild = mpimg.imread(bild_pfad)

# Bild als .npy-Datei speichern
np.save('bild.npy', bild)
print("Das Bild wurde als bild.npy gespeichert.")

import numpy as np
import matplotlib.pyplot as plt

# Datei laden
bild = np.load('bild.npy')

# Bild anzeigen
plt.imshow(bild)
plt.axis('off')
plt.show()
