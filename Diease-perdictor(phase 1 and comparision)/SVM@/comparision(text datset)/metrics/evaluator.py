# metrics/evaluator.py
import os
import numpy as np
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    auc,
    matthews_corrcoef,
    cohen_kappa_score
)
from sklearn.preprocessing import label_binarize

def evaluate_model(y_true, y_pred):
    """Basic metrics (keeps old API)."""
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="weighted", zero_division=0),
        "f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
    }

def compute_extended_metrics(y_true, y_pred, y_score=None, labels=None):
    """
    Compute extended metrics:
      - basic metrics (accuracy, precision, recall, f1)
      - confusion matrix
      - MCC (Matthews)
      - Cohen's Kappa
      - AUC (macro OVR) if y_score provided and usable
    y_score: either predict_proba (n_samples, n_classes) or decision_function output
    labels: list/array of class labels to use (optional)
    """
    results = evaluate_model(y_true, y_pred)
    if labels is None:
        labels = np.unique(np.concatenate([np.array(y_true), np.array(y_pred)]))

    # confusion, MCC, kappa
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    results["confusion_matrix"] = cm
    results["labels"] = list(labels)
    results["mcc"] = matthews_corrcoef(y_true, y_pred)
    results["kappa"] = cohen_kappa_score(y_true, y_pred)

    # AUC (best-effort)
    results["auc"] = None
    results["auc_error"] = None
    if y_score is not None:
        try:
            # If y_score is 1D (binary decision_function), compute binary AUC
            y_score_arr = np.array(y_score)
            if y_score_arr.ndim == 1:
                # Attempt binary roc
                results["auc"] = roc_auc_score(y_true, y_score_arr)
            else:
                # multiclass: try label_binarize + macro OVR
                y_true_bin = label_binarize(y_true, classes=labels)
                # If y_score has shape (n_samples, n_classes) we can compute multiclass AUC
                if y_score_arr.shape[1] == len(labels):
                    results["auc"] = roc_auc_score(y_true_bin, y_score_arr, average="macro", multi_class="ovr")
                else:
                    # Sometimes decision_function returns pairwise results; try to use predict_proba instead upstream
                    results["auc_error"] = "y_score has incompatible shape for multiclass AUC."
        except Exception as e:
            results["auc_error"] = str(e)
    return results

def _plot_confusion_matrix(cm, labels, outpath):
    plt.figure(figsize=(8, 6))
    im = plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar(im, fraction=0.046, pad=0.04)
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=90, fontsize=8)
    plt.yticks(tick_marks, labels, fontsize=8)
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def _plot_roc_multi(y_true, y_score, labels, outpath):
    """
    Macro-average ROC plotting for multiclass (OVR).
    y_true should be true labels (1D), y_score should be (n_samples, n_classes).
    """
    y_true_bin = label_binarize(y_true, classes=labels)
    n_classes = y_true_bin.shape[1]

    # store fpr/tpr/auc for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        try:
            fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        except Exception:
            fpr[i], tpr[i], roc_auc[i] = None, None, None

    # compute micro-average ROC curve and AUC
    # aggregate all fpr/tpr points
    # We'll compute a simple macro average for plot if possible
    plt.figure(figsize=(8, 6))
    for i in range(n_classes):
        if fpr[i] is not None:
            plt.plot(fpr[i], tpr[i], lw=1, alpha=0.3, label=f"Class {labels[i]} (AUC={roc_auc[i]:.2f})")
    plt.plot([0, 1], [0, 1], "k--", lw=1)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves (per-class)")
    plt.legend(loc="lower right", fontsize="small", ncol=1)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def print_metrics(results, title="Performance", save_dir="outputs", y_score=None):
    """
    Print metrics to console and save confusion matrix and ROC plots into save_dir.
    results: dictionary returned by compute_extended_metrics or evaluate_model
    y_score: optional score/probability matrix used for ROC plotting
    """
    os.makedirs(save_dir, exist_ok=True)
    print("=" * 60)
    print(title)
    print("-" * 60)
    # basic
    print(f"Accuracy : {results.get('accuracy', 0):.4f}")
    print(f"Precision: {results.get('precision', 0):.4f}")
    print(f"Recall   : {results.get('recall', 0):.4f}")
    print(f"F1       : {results.get('f1', 0):.4f}")

    # extended
    if "mcc" in results:
        print(f"MCC (Matthews Corr Coef): {results['mcc']:.4f}")
    if "kappa" in results:
        print(f"Cohen's Kappa         : {results['kappa']:.4f}")
    if "auc" in results:
        if results["auc"] is not None:
            print(f"AUC (macro OVR if multiclass): {results['auc']:.4f}")
        else:
            print("AUC: N/A", ("(", results.get("auc_error"), ")") if results.get("auc_error") else "")
    # confusion matrix
    if "confusion_matrix" in results and "labels" in results:
        print("\nConfusion Matrix:")
        print(results["confusion_matrix"])
        cm_path = os.path.join(save_dir, f"confusion_matrix_{title.replace(' ','_')}.png")
        try:
            _plot_confusion_matrix(results["confusion_matrix"], results["labels"], cm_path)
            print(f"Saved confusion matrix plot to: {cm_path}")
        except Exception as e:
            print("Failed to save confusion matrix plot:", e)

    # ROC plot (if y_score provided and shape matches)
    if y_score is not None and "labels" in results:
        roc_path = os.path.join(save_dir, f"roc_{title.replace(' ','_')}.png")
        try:
            y_score_arr = np.array(y_score)
            if y_score_arr.ndim == 1:
                # binary case: simple ROC
                fpr, tpr, _ = roc_curve(results.get("y_true_raw"), y_score_arr)
                roc_auc_val = auc(fpr, tpr)
                plt.figure()
                plt.plot(fpr, tpr, label=f"AUC = {roc_auc_val:.2f}")
                plt.plot([0, 1], [0, 1], "k--")
                plt.xlabel("False Positive Rate")
                plt.ylabel("True Positive Rate")
                plt.title("ROC Curve")
                plt.legend()
                plt.savefig(roc_path, dpi=200)
                plt.close()
                print(f"Saved ROC plot to: {roc_path}")
            else:
                # multiclass plotting (per-class)
                _plot_roc_multi(results.get("y_true_raw"), y_score_arr, results["labels"], roc_path)
                print(f"Saved multiclass ROC plot to: {roc_path}")
        except Exception as e:
            print("ROC plotting skipped: ", e)

    print("=" * 60)
