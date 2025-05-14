import numpy as np


def mean_of_frames(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    
    # Vérification que les longueurs correspondent
    min_len = min(len(y_true), len(y_pred))
    y_true, y_pred = y_true[:min_len], y_pred[:min_len]  # Tronque à la plus courte longueur
    
    accuracy = np.mean(y_true == y_pred)  # Calcul de la précision frame par frame
    return accuracy

