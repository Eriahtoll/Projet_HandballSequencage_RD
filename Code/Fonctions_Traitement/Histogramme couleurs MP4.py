import matplotlib.pyplot as plt

from Code.Fonctions_Traitement.FPS import *
input_path = r"../../Videos/testusamnice.mp4"
output_path = r"../../Videos/testusamnice15.mp4"
convert_video_to_fps(input_path, output_path)

# Charger la vidéo
video_path = r"../../Videos/testusamnice15.mp4"
cap = cv2.VideoCapture(video_path)

# Vérifier si la vidéo est bien chargée
if not cap.isOpened():
    print("Erreur lors du chargement de la vidéo")
    exit()

# Obtenir le framerate original de la vidéo
# fps_original = int(cap.get(cv2.CAP_PROP_FPS))
# frame_interval = (fps_original / 15)  # Intervalle pour atteindre 15 fps

frames = []
histograms = []

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Fin de la vidéo

    # Convertir en RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frames.append(frame_rgb)

    # Calculer l'histogramme des canaux R, G, B
    hist_data = []
    for i in range(3):  # 0: Rouge, 1: Vert, 2: Bleu
        hist = cv2.calcHist([frame_rgb], [i], None, [256], [0, 256])
        hist_data.append(hist)
    histograms.append(hist_data)

    frame_count += 1
print(frame_count)
print(histograms[45])
# Libérer la vidéo
cap.release()

# Afficher les images avec leurs histogrammes
plot_list = []

import pandas as pd

# Définir les intervalles d'intensité (0-9, 10-19, ..., 250-255)
bins = list(range(0, 257, 10))  # De 0 à 256 avec des pas de 10
bin_labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]

# Initialiser une liste pour stocker les données
data = []

for frame_idx, hist_data in enumerate(histograms):
    row = {"Frame": frame_idx + 1}  # Commencer à 1 pour la lisibilité
    for channel, color in enumerate(['Red', 'Green', 'Blue']):
        hist_values, _ = np.histogram(hist_data[channel], bins=bins)
        for i, value in enumerate(hist_values):
            row[f"{color}_{bin_labels[i]}"] = value
    data.append(row)

# Convertir en DataFrame
df = pd.DataFrame(data)

# Afficher les premières lignes pour vérifier
print(df.head())


for i, frame_rgb in enumerate(frames):
    # Créer une figure (avec mise en mémoire, pas d'affichage direct)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Afficher l'image
    axes[0].imshow(frame_rgb)
    axes[0].axis("off")
    axes[0].set_title(f"Frame {i+1}")

    # Afficher l'histogramme
    colors = ['r', 'g', 'b']
    for j, color in enumerate(colors):
        axes[1].plot(histograms[i][j], color=color)
    axes[1].set_xlim([0, 256])
    axes[1].set_ylim([0, 30000])
    axes[1].set_title("Histogramme RGB")

    # Sauvegarder la figure dans la liste (sans l'afficher)
    plt.show()


