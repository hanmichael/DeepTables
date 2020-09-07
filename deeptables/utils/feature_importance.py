# -*- coding:utf-8 -*-
__author__ = 'yangjian'
"""

"""

from eli5.permutation_importance import get_score_importances as eli5_importances
import pandas as pd
import numpy as np
from deeptables.models.evaluation import calc_score


def get_score_importances(dt_model, X, y, metric, n_iter=5, mode='min'):
    columns = X.columns.to_list()
    metric = metric.lower()

    def score(X_s, y_s) -> float:
        df = pd.DataFrame(X_s)
        df.columns = columns
        if metric in ['auc', 'log_loss']:
            y_proba = dt_model.predict_proba(df)
            y_pred = y_proba
        else:
            y_pred = dt_model.predict(df)
            y_proba = y_pred
        del df
        dict = calc_score(y_s, y_proba, y_pred, [metric], dt_model.task, dt_model.pos_label)
        print(f'score:{dict}')
        if mode == 'min':
            return -dict[metric]
        elif mode == 'max':
            return dict[metric]
        else:
            raise ValueError(f'Unsupported mode:{mode}')

    base_score, score_decreases = eli5_importances(score, X.values, y, n_iter=n_iter)
    feature_importances = np.stack([columns, np.mean(score_decreases, axis=0)], axis=1)
    return feature_importances
