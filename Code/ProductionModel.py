from Code.Fonctions_Traitement.FPS import*
from Code.Fonctions_Traitement.ColorHist30 import *
from Code.Fonctions_Traitement.DataFrame import *
from Code.Fonctions_Traitement.Graph import *
from Code.Metrique_Evaluation.IoU import *
from Code.Fonctions_Traitement.ChangementGaucheDroitMitemps import *
from Metrique_Evaluation.F1score import *


def VideotoCSV(
    video_path,
    video_fps_path,
    result_path,
    attaque_direction,
    mi_temps,
    fps=15,
    nb_intensity=30,
    temps_transition_gauche=2,
    temps_transition_droite=5,
    temps_action=11
):
    '''
    Cette fonction extrait automatiquement les phases de jeu (Attaque, Défense, Neutre) depuis une vidéo
    de handball en utilisant l'analyse d'histogrammes d'intensité. Les segments temporels détectés sont ensuite
    sauvegardés dans un fichier CSV au format (start, end, label), après prise en compte de la direction d’attaque.
    '''

    # Étape 1 : Conversion de la vidéo à une fréquence d'images fixe (si un chemin est donné)
    if video_path is not None:
        convert_video_to_fps(video_path, video_fps_path, fps)

    # Étape 2 : Création des histogrammes d’intensité à partir de la vidéo convertie
    histograms, total_frames = create_histograms_nb_intensity(video_fps_path, nb_intensity)

    # Étape 3 : Transformation des histogrammes en DataFrame pour exploitation
    df_histograms = Histograms_to_DF(histograms, nb_intensity, total_frames)

    # Étape 4 : Extraction de labels initiaux (Attaque/Défense) par traitement des histogrammes
    rough_labels = Df_to_List_Label(df_histograms, total_frames, smoothing_window=15)

    # Étape 5 : Ajout de segments "Neutre" pour lisser les transitions entre actions
    full_labels = List_Label_to_Neutre(
        rough_labels,
        temps_action,
        temps_transition_gauche,
        temps_transition_droite,
        fps
    )

    # Étape 6 : Regroupement des labels consécutifs en segments temporels (start, end, label)
    predicted_segments = LabelToSegment(full_labels)

    # Étape 7 : Conversion des segments en temps réel (en secondes ou horodatage lisible)
    SegmentToTime(predicted_segments, fps)

    # Étape 8 : Correction des segments selon la direction d’attaque initiale et le changement en mi-temps
    modifier_direction_equipe(predicted_segments, attaque_direction, mi_temps)

    # Étape 9 : Sauvegarde des segments prédits dans un fichier CSV (start, end, label)
    SegmentTemporeltoCSV(predicted_segments, result_path)



input_path = r"../Videos/J12COURT/J12Test310.mp4"
output_path_video = r"../Videos/J12COMPLET/J12complet5.mp4"
result_path = r"../CSV/CSVResults/result_J12Complet.csv"

VideotoCSV(None, output_path_video, result_path, 'gauche', 2140, fps=5)