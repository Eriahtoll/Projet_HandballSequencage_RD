import pandas as pd
import math
import csv

def SegmentTemporeltoCSV(segments, csv_path):
    """
    Transforme une liste de segments [start, end, label] en CSV et l'enregistre à l'emplacement donné.
    Ignore les segments avec le label 'Neutre'.
    Le temps est converti en millisecondes.
    """
    with open(csv_path, mode='w', newline='') as file:
        fieldnames = ['Nom', 'Position', 'Durée', 'Action', 'Défense', 'Rendement',
                      'Joueuses', 'Attaque', 'Défense Attaqué', 'Grand Espace']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for i, (start, end, label) in enumerate(segments):
            if label == 'Neutre':
                continue
            row = {
                'Nom': '',
                'Position': start * 1000,
                'Durée': (end - start) * 1000,
                'Action': '',
                'Défense': 1 if label == 'Défense' else '',
                'Rendement': '',
                'Joueuses': '',
                'Attaque': 1 if label == 'Attaque' else '',
                'Défense Attaqué': '',
                'Grand Espace': ''
            }
            writer.writerow(row)


def DftoTemporalSegment(df):
    """
    Convertit un DataFrame importé depuis un CSV en une liste de segments temporels.

    - Les "Grands Espaces" sont considérés comme des attaques.
    - La priorité est donnée au premier segment en cas de chevauchement.
    - Les espaces vides entre segments sont remplis avec le label 'Neutre'.
    """
    df = df[['Position', 'Durée:', 'Défense', 'Attaque', 'Grand Espace']]
    result = []

    for i, row in df.iterrows():
        position, duree, defense, attaque, ge = row
        end = math.ceil((position + duree) / 1000)
        position = math.ceil(position / 1000)

        if i == 0:
            if position > 0:
                result.append([0, position - 1, 'Neutre'])
        else:
            last_end = result[-1][1]
            if position > last_end + 1:
                result.append([last_end + 1, position - 1, 'Neutre'])
            else:
                position = last_end + 1

        if pd.notna(defense):
            result.append([position, end, 'Défense'])
        elif pd.notna(attaque) or pd.notna(ge):
            result.append([position, end, 'Attaque'])

    return result


def Histograms_to_DF(histograms, nb_intensity, frame_count):
    """
    Transforme une liste d’histogrammes en DataFrame.
    Utilise les 30 premiers pixels du canal bleu.
    """
    bins = list(range(0, nb_intensity + 10, 10))
    bin_labels = [f"{bins[i]}-{bins[i + 1] - 1}" for i in range(len(bins) - 1)]

    columns = ['Frame', 'Color'] + bin_labels
    data = []

    for i in range(frame_count):
        new_row = [i + 1, 'b']
        hist = histograms[i]

        for k in range(0, nb_intensity, 10):
            valeur = sum(hist[k:k + 10])
            new_row.append(valeur[0])  # [0] car OpenCV retourne des arrays [[valeur]]
        data.append(new_row)

    df = pd.DataFrame(data, columns=columns)
    df['Total'] = df.iloc[:, 2:].sum(axis=1)

    return df


def Df_to_List_Label(df, frame_count, smoothing_window=15):
    """
    Retourne une liste de labels "Gauche"/"Droite" par frame,
    en fonction de la moyenne de l’intensité et avec lissage.
    """
    labels_frames = []
    moyenne_globale = df['Total'].mean()

    for i in range(frame_count):
        label = "Droite" if df['Total'][i] >= moyenne_globale else "Gauche"
        labels_frames.append(label)

    labels_lissés = []
    for i in range(len(labels_frames)):
        debut = max(0, i - smoothing_window)
        fin = min(len(labels_frames), i + smoothing_window + 1)
        voisins = labels_frames[debut:i] + labels_frames[i + 1:fin]

        if not voisins:
            labels_lissés.append(labels_frames[i])
            continue

        gauche = voisins.count("Gauche")
        droite = voisins.count("Droite")
        nouveau_label = "Gauche" if gauche > droite else "Droite"
        labels_lissés.append(nouveau_label)

    return labels_lissés


def List_Label_to_Neutre(list_label_lisse, temps_action, temps_transition_action_gauche, temps_transition_action_droite, fps):
    """
    Insère des zones 'Neutres' entre les changements de direction selon les temps d'action et de transition.
    """
    nb_frames_action = fps * temps_action
    resultat = list_label_lisse.copy()
    i = 1
    dernier_changement = 0

    while i < len(list_label_lisse) - 1:
        if list_label_lisse[i] != list_label_lisse[i + 1]:
            if list_label_lisse[i] == 'Gauche':
                nb_frames_avant_action = fps * temps_transition_action_gauche
            else:
                nb_frames_avant_action = fps * temps_transition_action_droite

            fin_neutre_apres = i + 1
            debut_neutre_apres = max(dernier_changement + nb_frames_action, i - nb_frames_avant_action)

            fin_neutre_avant = max(dernier_changement + 1, i - nb_frames_avant_action - nb_frames_action)
            debut_neutre_avant = dernier_changement + 1

            for j in range(debut_neutre_avant, fin_neutre_avant):
                resultat[j] = "Neutre"
            for j in range(debut_neutre_apres, fin_neutre_apres):
                resultat[j] = "Neutre"

            dernier_changement = i
        i += 1

    return resultat