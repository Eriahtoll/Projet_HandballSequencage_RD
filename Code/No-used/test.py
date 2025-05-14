import pandas as pd
from Code.Fonctions_Traitement import Traitement_csv as trt
import MoF
import F1score as F1
from Code.Metrique_Evaluation import IoU
import Sursegmentation as S

# Annotations réelles
# Chaque ligne représente une phase de jeu avec son intervalle de frames et son label

df_true = pd.DataFrame([
    [0, 5, 0],  # Défense
    [6, 10, 1],  # Attaque
    [11, 15, 2],  # Phase neutre
    [16, 20, 1],  # Attaque
    [21, 25, 1]  # Attaque
], columns=['start_frame', 'end_frame', 'label'])

# Prédiction avec une séquence mal étiquetée
df_pred = pd.DataFrame([
    [0, 4, 0],  # Défense correcte sauf à la frame 5
    [5, 10, 1],  # Attaque correcte sauf la frame 5
    [11, 15, 2],  # Phase neutre correcte
    [16, 20, 1],  # Attaque correcte
    [21, 25, 2]  # Erreur: Phase neutre au lieu d'attaque
], columns=['start_frame', 'end_frame', 'label'])

# Prédiction avec sur-segmentation
df_pred2 = pd.DataFrame([
    [0, 5, 0],  # Défense
    [6, 7, 1],  # Attaque segmentée
    [8, 10, 1],  # Attaque segmentée
    [11, 15, 2],  # Phase neutre
    [16, 20, 1],  # Attaque
    [21, 25, 1]  # Attaque
], columns=['start_frame', 'end_frame', 'label'])

# Prédiction avec un décalage sur certaines frames
df_pred3 = pd.DataFrame([
    [0, 5, 0],  # Défense
    [6, 10, 1],  # Attaque
    [11, 13, 2],  # Phase neutre
    [14, 21, 1],  # Décalage ici (attaque)
    [22, 25, 1]  # Décalage ici (attaque)
], columns=['start_frame', 'end_frame', 'label'])

# Combinaison des défauts des trois prédictions
df_pred_combined = pd.DataFrame([
    [0, 4, 0],  # Défense correcte sauf à la frame 5
    [5, 7, 1],  # Attaque avec segmentation et mauvaise labellisation
    [8, 10, 1],  # Attaque segmentée
    [11, 13, 2],  # Phase neutre correcte
    [14, 21, 2],  # Mauvaise labellisation et décalage
    [22, 25, 2]  # Mauvaise labellisation et décalage
], columns=['start_frame', 'end_frame', 'label'])

# Expansion des labels frame par frame
y_true = trt.expand_labels(df_true)
y_preds = {
    "Mal étiqueté": trt.expand_labels(df_pred),
    "Sur-segmentation": trt.expand_labels(df_pred2),
    "Décalage": trt.expand_labels(df_pred3),
    "Combiné": trt.expand_labels(df_pred_combined)
}

# Calcul et affichage des métriques
for name, y_pred in y_preds.items():
    print(f"\n{name}:")
    print(f"Mean of Frames (MoF) Score: {MoF.mean_of_frames(y_true, y_pred):.2f}")

    f1_scores = F1.compute_f1_scores(y_true, y_pred)
    for metric, score in f1_scores.items():
        print(f"{metric}: {score:.4f}")

    iou_scores = IoU.compute_iou(y_true, y_pred)
    for metric, score in iou_scores.items():
        print(f"{metric}: {score:.4f}")

    print("\n")

print(f"Nombre de sur segment dans df_pred1 : {S.count_over_segmented_segments(df_true, df_pred)}")
print(f"Nombre de sur segment dans df_pred2 :{S.count_over_segmented_segments(df_true, df_pred2)}")
print(f"Nombre de sur segment dans df_pred3 : {S.count_over_segmented_segments(df_true, df_pred3)}")
print(f"Nombre de sur segment dans df_pred4 : {S.count_over_segmented_segments(df_true, df_pred_combined)}")