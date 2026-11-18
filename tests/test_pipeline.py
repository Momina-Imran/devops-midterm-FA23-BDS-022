import json
from pathlib import Path

import pandas as pd

import app
from train import fit_reference

CONFIG = json.loads(Path("config.json").read_text())


def test_metrics_fields_and_values():
    m = json.loads(Path("artifacts/metrics.json").read_text())
    for key in ("student_id", "accuracy", "training_rows", "model_version", "git_sha"):
        assert key in m
    assert m["student_id"] == CONFIG["student_id"]
    assert 0.0 < m["accuracy"] <= 1.0
    assert m["training_rows"] == len(pd.read_csv("dataset/train.csv"))


def test_model_trains_on_dataset():
    _, acc = fit_reference(pd.read_csv("dataset/train.csv"), CONFIG)
    assert 0.0 < acc <= 1.0


def test_metrics_endpoint_function():
    assert app.metrics()["student_id"] == CONFIG["student_id"]


def test_predict_returns_labels():
    rec = {f: 0.0 for f in CONFIG["features"]}
    out = app.predict(app.PredictionRequest(records=[rec]))
    assert out["predictions"][0] in (0, 1)