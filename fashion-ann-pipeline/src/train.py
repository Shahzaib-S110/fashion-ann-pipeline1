"""Build and train the ANN; save models/model.h5 and models/history.csv."""
import os
import numpy as np
import pandas as pd
import yaml
from tensorflow import keras

DATA, OUT = "data/processed", "models"

def main():
    p = yaml.safe_load(open("params.yaml"))["train"]
    tr = np.load(f"{DATA}/train.npz")
    val = np.load(f"{DATA}/val.npz")

    model = keras.Sequential([
        keras.layers.Input(shape=(28, 28)),
        keras.layers.Flatten(),
        keras.layers.Dense(p["dense_units"], activation="relu"),
        keras.layers.Dropout(p["dropout_rate"]),
        keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=p["learning_rate"]),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    history = model.fit(
        tr["x"], tr["y"],
        validation_data=(val["x"], val["y"]),
        epochs=p["epochs"], batch_size=p["batch_size"], verbose=2,
    )

    os.makedirs(OUT, exist_ok=True)
    model.save(f"{OUT}/model.h5")
    pd.DataFrame(history.history).to_csv(f"{OUT}/history.csv", index=False)
    print("Saved models/model.h5 and models/history.csv")

if __name__ == "__main__":
    main()
