import pandas as pd
from .config import DATASET_CSV, COLUMNS
import os

def ensure_csv_exists():
    os.makedirs(os.path.dirname(os.path.abspath(DATASET_CSV)), exist_ok=True)
    if not os.path.exists(DATASET_CSV):
        pd.DataFrame(columns=COLUMNS).to_csv(DATASET_CSV, index=False)

def append_rows(df_new):
    """
    Append new rows to the master CSV and return (added_count, total_rows_after).
    """
    ensure_csv_exists()
    df_old = pd.read_csv(DATASET_CSV)
    df_all = pd.concat([df_old, df_new], ignore_index=True)
    df_all.to_csv(DATASET_CSV, index=False)
    return len(df_new), len(df_all)
