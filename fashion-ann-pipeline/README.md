# fashion-ann-pipeline

Fully-connected ANN (no CNN) for Fashion-MNIST, versioned with Git + DVC (Google Drive remote).

## Pipeline
prepare -> preprocess -> train -> evaluate  (see `dvc.yaml`, hyperparameters in `params.yaml`)

## Run
    pip install -r requirements.txt
    dvc repro
