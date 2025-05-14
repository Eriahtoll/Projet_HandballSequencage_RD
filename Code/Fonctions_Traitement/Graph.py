import plotly.graph_objects as go
import pandas as pd
from matplotlib import pyplot as plt

import plotly.graph_objects as go

def visualize_segment_comparison(segments1, segments2):
    def convert_segments_to_label_list(segments):
        # Trouver la longueur max pour la timeline
        max_end = max(end for start, end, _ in segments)
        labels = [""] * (max_end + 1)

        for start, end, label in segments:
            for i in range(start, end + 1):
                if 0 <= i < len(labels):
                    labels[i] = label
        return labels

    def labels_to_numeric(labels):
        mapping = {"Défense": 0, "Neutre": 1, "Attaque": 2}
        return [mapping.get(label, 1) for label in labels]  # Neutre par défaut

    # Transformer les segments en listes complètes de labels
    labels1 = convert_segments_to_label_list(segments1)
    labels2 = convert_segments_to_label_list(segments2)

    # S'assurer que les deux listes ont la même longueur
    max_len = max(len(labels1), len(labels2))
    labels1 += ["Neutre"] * (max_len - len(labels1))
    labels2 += ["Neutre"] * (max_len - len(labels2))

    y1 = labels_to_numeric(labels1)
    y2 = labels_to_numeric(labels2)
    x = list(range(max_len))

    # Création de la figure Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y1,
        mode='lines',
        line_shape='hv',
        name='SegmentRéel',
        line=dict(color='royalblue')
    ))

    fig.add_trace(go.Scatter(
        x=x,
        y=y2,
        mode='lines',
        line_shape='hv',
        name='SegmentPrédit',
        line=dict(color='orangered')
    ))

    fig.update_layout(
        title="Comparaison des phases : Réel vs Prédit",
        xaxis_title="Temps (frames)",
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2],
            ticktext=['Défense', 'Neutre', 'Attaque']
        ),
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=40, b=40),
    )

    fig.show()

def Show_DF_Histograms(df, nb_intensity):
    # Filtrage et calcul
    moyenne_globale = df['Total'].mean()

    # Création du graphique interactif
    fig = go.Figure()

    # Ajout de la courbe moyenne
    fig.add_trace(go.Scatter(x=df['Frame'], y=df['Total'],
                             mode='lines', name='Moyenne'))

    # Ligne horizontale pour la moyenne globale
    fig.add_trace(go.Scatter(x=[df['Frame'].min(), df['Frame'].max()],
                             y=[moyenne_globale, moyenne_globale],
                             mode='lines',
                             line=dict(dash='dash', color='red'),
                             name='Moyenne globale'))

    # Mise en forme
    fig.update_layout(title=f'Évolution Nb Pixel (Intensité <{nb_intensity})',
                      xaxis_title='Frame',
                      yaxis_title=f'Nb Pixel (Intensité <{nb_intensity})',
                      hovermode='x unified')

    # Affichage
    fig.show()

def Show_Phases(labels_with_neutres):
    # Conversion des labels en valeurs numériques
    valeurs = [0 if label == "Gauche" else 1 if label == "Neutre" else 2 for label in labels_with_neutres]
    x = list(range(len(labels_with_neutres)))

    # Création de la figure Plotly
    fig = go.Figure()

    # Ajout de la courbe avec steps-post
    fig.add_trace(go.Scatter(
        x=x,
        y=valeurs,
        mode='lines+markers',
        line_shape='hv',  # 'hv' pour "horizontal-vertical" = steps-post
        name='Position',
        line=dict(color='blue')
    ))

    # Personnalisation des axes
    fig.update_layout(
        title="Position gauche/neutre/droite",
        xaxis_title="Index",
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2],
            ticktext=['gauche', 'neutre', 'droite']
        ),
        height=300,
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
    )

    # Affichage
    fig.show()