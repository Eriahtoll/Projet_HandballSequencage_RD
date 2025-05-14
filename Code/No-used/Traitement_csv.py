import pandas as pd

def expand_labels(df):  
    labels = {}
    for _, row in df.iterrows():
        start, end, label = row
        for frame in range(start, end + 1):
            labels[frame] = label  # Affecte le label à chaque frame

    # Retourne une liste triée des labels (par indice de frame)
    max_frame = max(labels.keys(), default=0)  # Sécurise si aucun frame
    return [labels.get(frame, 2) for frame in range(max_frame + 1)]  # Par défaut, neutre (2)