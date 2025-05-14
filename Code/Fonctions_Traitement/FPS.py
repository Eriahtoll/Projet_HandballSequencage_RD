import moviepy
import cv2
import os
import re

def convert_video_to_fps(input_path, output_path, fps=15):
    '''
    Convertit une vidéo en modifiant son nombre d'images par seconde (fps).
    Si la vidéo est déjà au fps souhaité, aucune action n'est effectuée.

    Paramètres :
        input_path : str - chemin de la vidéo source
        output_path : str - chemin de la vidéo convertie
        fps : int - nombre d'images par seconde souhaité (par défaut : 15)
    '''
    video = moviepy.VideoFileClip(input_path)

    if video.fps != fps:
        video_15fps = video.with_fps(fps)
        video_15fps.write_videofile(output_path, codec="libx264", audio_codec="aac")
        video_15fps.close()
    else:
        print("La vidéo est déjà à 15 fps. Aucune conversion nécessaire.")

    video.close()

def extract_number(filename):
    '''
    Extrait le premier nombre présent dans un nom de fichier (utilisé pour trier des images par ordre numérique).

    Paramètres :
        filename : str - nom du fichier

    Retour :
        int - le premier nombre extrait ou 0 si aucun nombre n'est trouvé
    '''
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else 0

def create_video3(input_folder, output_video, fps=15):
    '''
    Crée une vidéo à partir d'une série d'images (.png ou .jpg) dans un dossier, triées par numéro.

    Paramètres :
        input_folder : str - dossier contenant les images
        output_video : str - chemin du fichier vidéo de sortie
        fps : int - images par seconde (par défaut : 15)
    '''
    # Récupération et tri des images dans le dossier
    images = sorted(
        [img for img in os.listdir(input_folder) if img.endswith(".png") or img.endswith(".jpg")],
        key=extract_number)

    # Lecture de la première image pour obtenir les dimensions
    frame = cv2.imread(os.path.join(input_folder, images[0]))
    h, w, _ = frame.shape

    # Initialisation du writer vidéo
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_video, fourcc, fps, (w, h))

    # Écriture de chaque image dans la vidéo
    for image in images:
        img_path = os.path.join(input_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    video.release()
    print(f"Vidéo créée: {output_video}")

def LabelToSegment(listelabels):
    '''
    Transforme une séquence de labels image par image en segments continus de même classe.

    Paramètres :
        listelabels : List[str] - liste de labels image par image (frame par frame)

    Retour :
        List[List[int, int, str]] - liste de segments au format [début, fin, label]
    '''
    nb = 0
    label = listelabels[0]
    result = []
    for i in range(len(listelabels)):
        if listelabels[i] != label:
            result.append([i - nb, i - 1, label])  # fin du segment précédent
            label = listelabels[i]
            nb = 0
        if i == (len(listelabels) - 1):
            result.append([i - nb, i + 1, label])  # dernier segment
        nb += 1

    return result

def SegmentToTime(listeSegment, fps):
    '''
    Convertit des indices de segments exprimés en frames en temps exprimé en secondes.
    La fonction modifie la liste fournie **en place**.

    Paramètres :
        listeSegment : List[List[int, int, str]] - segments [début_frame, fin_frame, label]
        fps : int - nombre d'images par seconde
    '''
    # Conversion du premier segment
    indice0 = 0
    indice1 = listeSegment[0][1] // fps
    listeSegment[0][1] = indice1
    listeSegment[0][0] = indice0

    # Conversion des segments suivants
    for i in range(1, len(listeSegment)):
        indice1 = listeSegment[i][1] // fps
        indice0 = listeSegment[i - 1][1] + 1
        listeSegment[i][1] = indice1
        listeSegment[i][0] = indice0