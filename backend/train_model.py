from pathlib import Path
import json
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

BASE = Path(__file__).parent
DATA = BASE / "data" / "crop_recommendation.csv"
MODEL_DIR = BASE / "models"
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

def main():
    if not DATA.exists():
        raise SystemExit("Dataset not found. Run: python generate_demo_data.py")
    df = pd.read_csv(DATA)
    required = FEATURES + ["label"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"Dataset missing columns: {missing}")
    df = df[required].dropna()
    if df["label"].nunique() < 2:
        raise SystemExit("At least two crop labels are required.")
    X, y = df[FEATURES], df["label"].astype(str)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    candidates = {
        "Random Forest": RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced"),
        "Decision Tree": DecisionTreeClassifier(max_depth=12, random_state=42, class_weight="balanced"),
    }
    results = {}
    best_name, best_model, best_acc = None, None, -1
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        metrics = {
            "accuracy": round(accuracy_score(y_test, pred), 4),
            "precision": round(precision_score(y_test, pred, average="weighted", zero_division=0), 4),
            "recall": round(recall_score(y_test, pred, average="weighted", zero_division=0), 4),
            "f1": round(f1_score(y_test, pred, average="weighted", zero_division=0), 4),
        }
        results[name] = metrics
        if metrics["accuracy"] > best_acc:
            best_name, best_model, best_acc = name, model, metrics["accuracy"]
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump({"model": best_model, "features": FEATURES, "model_name": best_name}, MODEL_DIR / "crop_model.joblib")
    payload = {
        "selected_model": best_name,
        "dataset_rows": int(len(df)),
        "crop_count": int(y.nunique()),
        "metrics": results,
        "note": "Metrics are from a held-out split. Interpret in the context of dataset quality."
    }
    (MODEL_DIR / "metrics.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
