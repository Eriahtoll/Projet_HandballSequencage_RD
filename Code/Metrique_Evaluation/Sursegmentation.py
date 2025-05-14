import pandas as pd
import numpy as np


def count_over_segmented_segments(df_true, df_pred):
    over_segmented_counts = []
    for _, true_row in df_true.iterrows():
        start, end, label = true_row
        matching_segments = df_pred[((df_pred['start_frame'] >= start) & (df_pred['start_frame'] <=end) | (df_pred['end_frame'] >= start) & (df_pred['end_frame'] <= end)) & (df_pred['label'] == label)]
        count = len(matching_segments) - 1 if len(matching_segments) > 1 else 0
        over_segmented_counts.append(count)
    return sum(over_segmented_counts)