"""Normalize to [0, 1], split validation set, save to data/processed/."""
import os
import numpy as np
import yaml
from sklearn.model_selection import train_test_split

RAW, OUT = "data/raw", "data/processed"

def main():
    params = yaml.safe_load(open("params.yaml"))["preprocess"]
    train = np.load(f"{RAW}/train.npz")
    test = np.load(f"{RAW}/test.npz")

    x_train = train["x"].astype("float32") / 255.0
    x_test = test["x"].astype("float32") / 255.0

    x_tr, x_val, y_tr, y_val = train_test_split(
        x_train, train["y"],
        test_size=params["test_size"],
        random_state=params["seed"],
        stratify=train["y"],
    )

    os.makedirs(OUT, exist_ok=True)
    np.savez_compressed(f"{OUT}/train.npz", x=x_tr, y=y_tr)
    np.savez_compressed(f"{OUT}/val.npz", x=x_val, y=y_val)
    np.savez_compressed(f"{OUT}/test.npz", x=x_test, y=test["y"])
    print(f"train {x_tr.shape}, val {x_val.shape}, test {x_test.shape}")

if __name__ == "__main__":
    main()
