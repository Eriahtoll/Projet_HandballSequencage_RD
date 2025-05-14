import cv2

def create_histograms_nb_intensity(video_fps_path, nb_intensity):
    """
    Extrait les histogrammes du canal bleu d'une vidéo, en ne conservant que les nb_intensity premières valeurs.

    :param video_fps_path: Chemin vers la vidéo
    :param nb_intensity: Nombre de niveaux d'intensité à considérer (ex. 30 pour 0-29)
    :return: Tuple (liste des histogrammes, nombre total de frames)
    """
    cap = cv2.VideoCapture(video_fps_path)

    # Vérifier que la vidéo est bien ouverte
    if not cap.isOpened():
        print("Erreur lors du chargement de la vidéo")
        exit()

    histograms = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Fin de la vidéo

        # Calcul de l'histogramme sur le canal bleu (canal 0 en BGR)
        hist = cv2.calcHist([frame], [0], None, [nb_intensity], [0, nb_intensity])
        histograms.append(hist)

        frame_count += 1

    cap.release()
    return histograms, frame_count