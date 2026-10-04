"""Evaluate on the test set; write metrics.json and a confusion matrix image."""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tensorflow import keras

CLASSES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
           "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

def main():
    model = keras.models.load_model("models/model.h5")
    test = np.load("data/processed/test.npz")
    loss, acc = model.evaluate(test["x"], test["y"], verbose=0)

    preds = np.argmax(model.predict(test["x"], verbose=0), axis=1)
    cm = confusion_matrix(test["y"], preds)
    fig, ax = plt.subplots(figsize=(8, 8))
    ConfusionMatrixDisplay(cm, display_labels=CLASSES).plot(
        ax=ax, xticks_rotation=45, colorbar=False)
    plt.tight_layout()
    os.makedirs("reports", exist_ok=True)
    fig.savefig("reports/confusion_matrix.png", dpi=120)

    with open("metrics.json", "w") as f:
        json.dump({"test_loss": float(loss), "test_accuracy": float(acc)}, f, indent=2)
    print(f"test_loss={loss:.4f} test_accuracy={acc:.4f}")

if __name__ == "__main__":
    main()
