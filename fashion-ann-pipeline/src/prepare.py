"""Download Fashion-MNIST and save raw arrays to data/raw/."""
import os
import numpy as np
from tensorflow import keras

OUT = "data/raw"

def main():
    os.makedirs(OUT, exist_ok=True)
    (x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
    np.savez_compressed(f"{OUT}/train.npz", x=x_train, y=y_train)
    np.savez_compressed(f"{OUT}/test.npz", x=x_test, y=y_test)
    print(f"Saved raw data: train {x_train.shape}, test {x_test.shape}")

if __name__ == "__main__":
    main()
