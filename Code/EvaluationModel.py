from Code.Fonctions_Traitement.FPS import*
from Code.Fonctions_Traitement.ColorHist30 import *
from Code.Fonctions_Traitement.DataFrame import *
from Code.Fonctions_Traitement.Graph import *
from Code.Metrique_Evaluation.IoU import *
from Code.Fonctions_Traitement.ChangementGaucheDroitMitemps import *
from Metrique_Evaluation.F1score import *


def VideotoScore(
    video_path,
    video_fps_path,
    csv_path,
    attaque_direction,
    mi_temps,
    fps=15,
    nb_intensity=30,
    temps_transition_gauche=2,
    temps_transition_droite=5,
    temps_action=11
):
    '''
    Cette fonction analyse une vidéo de match de handball pour en extraire automatiquement les phases de jeu
    ("Attaque", "Défense") à partir d'histogrammes d'intensité d'image, puis les compare aux annotations
    humaines disponibles dans un fichier CSV. Elle affiche et évalue la qualité de la segmentation automatique
    (IoU, F1-score).
    '''

    # Étape 1 : Conversion de la vidéo à une fréquence d'images fixe (si un chemin est donné)
    if video_path is not None:
        convert_video_to_fps(video_path, video_fps_path, fps)

    # Étape 2 : Création des histogrammes d'intensité à "nb_intensity" classes
    histograms, total_frames = create_histograms_nb_intensity(video_fps_path, nb_intensity)

    # Étape 3 : Transformation des histogrammes en DataFrame pour traitement
    df_histograms = Histograms_to_DF(histograms, nb_intensity, total_frames)

    # Étape 4 : Visualisation des histogrammes sous forme de courbes
    Show_DF_Histograms(df_histograms, nb_intensity)

    # Étape 5 : Extraction d'une première série de labels (phases) lissée à partir des histogrammes
    rough_labels = Df_to_List_Label(df_histograms, total_frames, smoothing_window=15)

    # Étape 6 : Ajout des phases "Neutre" entre transitions et actions
    full_labels = List_Label_to_Neutre(
        rough_labels,
        temps_action,
        temps_transition_gauche,
        temps_transition_droite,
        fps
    )

    # Étape 7 : Transformation de la liste de labels en segments temporels (start, end, label)
    predicted_segments = LabelToSegment(full_labels)

    # Étape 8 : Affichage de ces segments avec le temps réel (secondes)
    SegmentToTime(predicted_segments, fps)

    # Étape 9 : Affichage visuel des phases dans le temps
    Show_Phases(full_labels)

    # Étape 10 : Correction des segments en fonction de la direction d’attaque et de la mi-temps
    modifier_direction_equipe(predicted_segments, attaque_direction, mi_temps)

    # Étape 11 : Lecture des annotations humaines depuis le fichier CSV
    df_ground_truth = pd.read_csv(csv_path)

    # Étape 12 : Transformation des annotations humaines en segments temporels
    ground_truth_segments = DftoTemporalSegment(df_ground_truth)

    #Étape 13 : On enlève les prédictions de fin de match (célébrations/remise de prix...)
    i = len(predicted_segments)-1
    while predicted_segments[i][0] > ground_truth_segments[-1][1] :
        predicted_segments.remove(predicted_segments[i])
        i = i - 1

    # Étape 14 : Affichage comparatif des segments prédits vs. vérité terrain
    visualize_segment_comparison(ground_truth_segments, predicted_segments)

    # Étape 15 : Évaluation avec une métrique personnalisée (ex. Jaccard ajusté)
    IOU_modified(ground_truth_segments, predicted_segments)

    # Étape 16 : Calcul de l’IoU par label avec affichage clair
    IOU_classique(predicted_segments, ground_truth_segments)

    # Étape 17 : Calcul des F1-scores par label avec affichage et moyenne brute
    F1_Classic(ground_truth_segments, predicted_segments, ['Neutre', 'Attaque', 'Défense'])


input_path = r"../Videos/USAM vs CANNES.mp4"
output_path_video15 = r"../Videos/USAM vs CANNES5.mp4"
csv_path = r"../CSV/J17 USAM vs CANNES-1.csv"

VideotoScore(input_path,
             output_path_video15,
             csv_path,
             'gauche',
             2160,
             fps=5,
             temps_transition_gauche=1,
             temps_transition_droite=7)
