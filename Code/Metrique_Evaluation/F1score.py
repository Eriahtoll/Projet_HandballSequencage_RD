def F1_Classic(true_segments, pred_segments, labels=None):
    '''
    Calcule les scores de précision, rappel et F1 pour chaque label présent
    dans les segments temporels vrais (`true_segments`) et prédits (`pred_segments`).
    Affiche également une moyenne brute du F1-score pour les labels "Attaque" et "Défense".

    Paramètres :
        true_segments : List[Tuple[int, int, str]] - segments vrais (début, fin, label)
        pred_segments : List[Tuple[int, int, str]] - segments prédits (début, fin, label)
        labels : List[str] ou None - liste des labels à évaluer (calculée automatiquement si None)

    Retour :
        results : dict - dictionnaire contenant précision, rappel, F1, TP, FP et FN pour chaque label
    '''

    # Si les labels ne sont pas fournis, on les extrait automatiquement des deux listes de segments
    if labels is None:
        labels = list(set([s[2] for s in true_segments + pred_segments]))

    # Détermination de la longueur maximale pour créer les timelines
    max_time = max(max(s[1] for s in true_segments), max(s[1] for s in pred_segments))

    # Initialisation des timelines pour chaque seconde avec le label 'None'
    true_timeline = ['None'] * (max_time + 1)
    pred_timeline = ['None'] * (max_time + 1)

    # Remplissage de la timeline réelle avec les labels correspondants
    for start, end, label in true_segments:
        for t in range(start, end + 1):
            true_timeline[t] = label

    # Remplissage de la timeline prédite avec les labels correspondants
    for start, end, label in pred_segments:
        for t in range(start, end + 1):
            pred_timeline[t] = label

    # Calcul des métriques pour chaque label
    results = {}
    for label in labels:
        TP = sum((t == label and p == label) for t, p in zip(true_timeline, pred_timeline))  # Vrai Positifs
        FP = sum((t != label and p == label) for t, p in zip(true_timeline, pred_timeline))  # Faux Positifs
        FN = sum((t == label and p != label) for t, p in zip(true_timeline, pred_timeline))  # Faux Négatifs

        precision = TP / (TP + FP) if (TP + FP) > 0 else 0  # Précision
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0      # Rappel
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0  # Score F1

        results[label] = {'precision': precision, 'recall': recall, 'f1': f1, 'TP': TP, 'FP': FP, 'FN': FN}

    # Affichage détaillé des scores pour chaque label
    print("\n=== F1 Score ===")
    for label in labels:
        res = results[label]
        print(f"Label : {label}")
        print(f"  - Précision : {res['precision']:.3f}")
        print(f"  - Rappel     : {res['recall']:.3f}")
        print(f"  - F1-score   : {res['f1']:.3f}")
        print(f"  - TP : {res['TP']}, FP : {res['FP']}, FN : {res['FN']}")
        print("")

    # Calcul de la moyenne brute des F1 scores pour "Attaque" et "Défense"
    f1_scores = [results[label]['f1'] for label in ['Attaque', 'Défense'] if label in results]
    if f1_scores:
        average_f1 = sum(f1_scores) / len(f1_scores)
        print(f"=== Moyenne brute des F1 scores ('Attaque' et 'Défense') : {average_f1:.3f} ===")
    else:
        print("=== Labels 'Attaque' et 'Défense' non trouvés dans les résultats ===")

    return results