from typing import List, Tuple

def IOU_modified(true_list, pred_list):
    '''
    Calcule une version modifiée du score d'Intersection over Union (IoU) pour évaluer la précision
    des segments temporels prédits par rapport aux segments réels, en tenant compte des labels.
    Retourne les scores IoU pour les labels "Neutre", "Défense", "Attaque" ainsi qu'un score moyen suivant Attaque/Défense.
    '''
    score_neutre = 0
    nb_neutre = 0
    score_defense = 0
    nb_defense = 0
    score_attaque = 0
    nb_attaque = 0

    # Parcours de chaque segment réel
    for true_segment in true_list:
        begin, end, label = true_segment[0], true_segment[1], true_segment[2]
        segments = []

        # Recherche des segments prédits ayant le même label et qui se chevauchent
        for pred_segment in pred_list:
            pred_begin, pred_end, pred_label = pred_segment[0], pred_segment[1], pred_segment[2]
            if pred_label == label:
                if pred_begin > end:
                    break  # Si le début du segment prédit dépasse la fin du vrai, on sort
                if begin <= pred_begin <= end:
                    segments.append([pred_segment, min(pred_end, end) - pred_begin])
                elif begin <= pred_end <= end:
                    segments.append([pred_segment, pred_end - max(begin, pred_begin)])

        # Sélection du meilleur segment prédit
        if len(segments) > 1:
            segments.sort(key=lambda x: x[1])  # Trie par durée de chevauchement
            segment = segments[-1]
        elif len(segments) == 0:
            nb_neutre += 1  # Aucun segment prédit correspondant
            continue
        else:
            segment = segments[0]

        # Calcul du score IoU pour le label correspondant
        if label == 'Neutre':
            if (max(end, segment[0][1]) - min(begin, segment[0][0])) != 0:
                score_neutre += segment[1] / (max(end, segment[0][1]) - min(begin, segment[0][0]))
            nb_neutre += 1
        if label == 'Défense':
            score_defense += segment[1] / (max(end, segment[0][1]) - min(begin, segment[0][0]))
            nb_defense += 1
        if label == 'Attaque':
            score_attaque += segment[1] / (max(end, segment[0][1]) - min(begin, segment[0][0]))
            nb_attaque += 1

    # Calcul des moyennes
    IOU_neutre = score_neutre / nb_neutre
    IOU_defense = score_defense / nb_defense
    IOU_attaque = score_attaque / nb_attaque
    IOU_mean = (IOU_defense + IOU_attaque) / 2

    # Affichage des résultats
    print(f"=== Score IOU Modifié === : \n"
          f"Score  Défense = {IOU_defense}\n"
          f" Score Attaque = {IOU_attaque}\n"
          f" Score Moyen = {IOU_mean}")

    return IOU_neutre, IOU_defense, IOU_attaque, IOU_mean



def IOU_classique(preds: List[Tuple[int, int, str]], gts: List[Tuple[int, int, str]]) -> dict:
    '''
    Calcule le score classique d'Intersection over Union (IoU) entre des segments prédits et réels,
    pour chaque label. Retourne un dictionnaire contenant les scores IoU par label.
    '''
    # Fonction interne pour calculer intersection et union entre deux masques binaires
    def get_union_and_intersection(label: str):
        # Déterminer la longueur maximale en secondes
        max_time = max(
            max((end for start, end, _ in preds), default=0),
            max((end for start, end, _ in gts), default=0)
        ) + 1

        # Création de masques binaires pour prédictions et ground truths
        pred_mask = [0] * max_time
        gt_mask = [0] * max_time

        for start, end, lbl in preds:
            if lbl == label:
                for t in range(start, end + 1):
                    pred_mask[t] = 1

        for start, end, lbl in gts:
            if lbl == label:
                for t in range(start, end + 1):
                    gt_mask[t] = 1

        # Calcul de l'intersection et de l'union
        intersection = sum(p & g for p, g in zip(pred_mask, gt_mask))
        union = sum(p | g for p, g in zip(pred_mask, gt_mask))

        return intersection, union

    # Récupération des labels uniques dans les deux listes
    labels = set(lbl for _, _, lbl in preds) | set(lbl for _, _, lbl in gts)
    iou_per_label = {}

    # Calcul du IoU par label
    for label in labels:
        inter, union = get_union_and_intersection(label)
        iou = inter / union if union > 0 else 0.0
        iou_per_label[label] = iou

    # Affichage des détails par label
    print("\n=== IoU classique ===")
    for label in labels:
        inter, union = get_union_and_intersection(label)
        iou = inter / union if union > 0 else 0.0
        iou_per_label[label] = iou
        print(f"Label : {label}")
        print(f"  - Intersection : {inter}")
        print(f"  - Union        : {union}")
        print(f"  - IoU          : {iou:.3f}")
        print("")

    # Calcul et affichage de la moyenne brute pour "Attaque" et "Défense"
    relevant_labels = ['Attaque', 'Défense']
    iou_scores = [iou_per_label[label] for label in relevant_labels if label in iou_per_label]
    if iou_scores:
        avg_iou = sum(iou_scores) / len(iou_scores)
        print(f"=== Moyenne brute des IoU ('Attaque' et 'Défense') : {avg_iou:.3f} ===")
    else:
        print("=== Labels 'Attaque' et 'Défense' non trouvés dans les résultats ===")

    return iou_per_label