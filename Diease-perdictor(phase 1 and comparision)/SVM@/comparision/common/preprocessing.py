import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data(path, n_samples=None):
    """
    Load and preprocess the cardiovascular dataset.

    Parameters:
    - path: str, path to the dataset file.
    - n_samples: int or None, number of rows to sample from the dataset.
                 If None, use the entire dataset.

    Returns:
    - X_train, X_test, y_train, y_test: preprocessed and split data.
    """
    df = pd.read_csv(path, sep=';')
    df['age'] = df['age'] // 365  # convert age from days to years

    # Downsample if needed
    if n_samples is not None:
        df = df.sample(n=n_samples, random_state=42)

    X = df.drop(columns=["cardio"])
    y = df["cardio"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return train_test_split(X_scaled, y, test_size=0.2, random_state=42)
