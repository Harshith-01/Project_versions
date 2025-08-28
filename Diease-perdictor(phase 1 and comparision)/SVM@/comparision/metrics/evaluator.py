from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    matthews_corrcoef,
    cohen_kappa_score,
    confusion_matrix
)
import numpy as np

def evaluate_model(y_true, y_pred):
    # For ROC AUC, need probabilities or decision function if binary
    try:
        roc_auc = roc_auc_score(y_true, y_pred)
    except ValueError:
        roc_auc = np.nan

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "roc_auc": roc_auc,
        "matthews_corrcoef": matthews_corrcoef(y_true, y_pred),
        "cohen_kappa": cohen_kappa_score(y_true, y_pred),
        "confusion_matrix": confusion_matrix(y_true, y_pred)
    }

def print_metrics(metrics):
    for k, v in metrics.items():
        if k == "confusion_matrix":
            print(f"{k.capitalize()}:\n{v}")
        else:
            print(f"{k.capitalize()}: {v:.4f}" if isinstance(v, (int, float)) else f"{k.capitalize()}: {v}")
