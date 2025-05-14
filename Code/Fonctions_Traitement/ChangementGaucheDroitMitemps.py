def modifier_direction_equipe(real_time, attaque_direction, mi_temps):
    """
    Modifie la direction d'attaque et de défense dans la liste des intervalles en fonction de la mi-temps
    et de la direction d'attaque choisie.

    :param real_time: Liste des intervalles [start, end, label] représentant les phases de jeu
    :param attaque_direction: Direction de l'attaque, soit "gauche", soit "droite"
    :param mi_temps: Temps de la mi-temps pour séparer les phases avant et après
    """
    if attaque_direction == "gauche":
        # Avant la mi-temps : "Gauche" = "Attaque" et "Droite" = "Défense"
        for intervalle in real_time:
            if intervalle[1] <= mi_temps:  # Avant mi-temps
                if intervalle[2] == 'Gauche':
                    intervalle[2] = 'Attaque'
                elif intervalle[2] == 'Droite':
                    intervalle[2] = 'Défense'
            else:  # Après mi-temps
                if intervalle[2] == 'Gauche':
                    intervalle[2] = 'Défense'
                elif intervalle[2] == 'Droite':
                    intervalle[2] = 'Attaque'
    elif attaque_direction == "droite":
        # Avant la mi-temps : "Gauche" = "Défense" et "Droite" = "Attaque"
        for intervalle in real_time:
            if intervalle[1] <= mi_temps:  # Avant mi-temps
                if intervalle[2] == 'Gauche':
                    intervalle[2] = 'Défense'
                elif intervalle[2] == 'Droite':
                    intervalle[2] = 'Attaque'
            else:  # Après mi-temps
                if intervalle[2] == 'Gauche':
                    intervalle[2] = 'Attaque'
                elif intervalle[2] == 'Droite':
                    intervalle[2] = 'Défense'
    else:
        print("Direction invalide. Veuillez répondre par 'gauche' ou 'droite'.")