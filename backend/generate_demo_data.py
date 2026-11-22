"""Create clearly-labelled synthetic rows for UI and integration testing only."""
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).parent / "data" / "crop_recommendation.csv"
rng = np.random.default_rng(42)
# Approximate feature centres are only synthetic fixtures, not crop prescriptions.
centres = {
    "rice": [80, 45, 40, 25, 82, 6.2, 220],
    "maize": [75, 45, 35, 24, 65, 6.5, 90],
    "chickpea": [40, 65, 80, 20, 18, 7.1, 65],
    "kidneybeans": [20, 65, 20, 20, 22, 5.8, 105],
    "pigeonpeas": [20, 65, 20, 28, 48, 6.2, 150],
    "mothbeans": [20, 45, 20, 30, 50, 6.8, 55],
    "mungbean": [20, 45, 20, 28, 85, 6.8, 50],
    "blackgram": [40, 60, 20, 30, 65, 7.1, 70],
    "lentil": [20, 65, 20, 22, 65, 6.9, 45],
    "pomegranate": [20, 10, 40, 22, 90, 6.5, 110],
    "banana": [100, 80, 50, 27, 80, 6.0, 105],
    "mango": [20, 25, 30, 31, 50, 5.8, 95],
    "grapes": [20, 125, 200, 24, 82, 6.0, 70],
    "watermelon": [100, 10, 50, 26, 85, 6.5, 50],
    "muskmelon": [100, 20, 50, 28, 90, 6.5, 35],
    "apple": [20, 135, 200, 22, 90, 6.0, 115],
    "orange": [20, 10, 10, 24, 90, 7.0, 110],
    "papaya": [50, 50, 50, 33, 90, 6.5, 140],
    "coconut": [20, 10, 30, 27, 95, 5.8, 180],
    "cotton": [120, 45, 20, 24, 80, 6.5, 80],
    "jute": [80, 45, 40, 25, 80, 6.5, 175],
    "coffee": [100, 20, 30, 25, 60, 6.0, 160],
}
rows = []
scales = [8, 10, 10, 2.5, 7, 0.35, 18]
for label, centre in centres.items():
    for _ in range(65):
        vals = np.array(centre) + rng.normal(0, scales)
        vals[0:3] = np.clip(vals[0:3], 0, 140)
        vals[3] = np.clip(vals[3], 8, 45)
        vals[4] = np.clip(vals[4], 10, 100)
        vals[5] = np.clip(vals[5], 3.5, 9.5)
        vals[6] = np.clip(vals[6], 20, 300)
        rows.append([*vals.round(2), label])
OUT.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows, columns=["N","P","K","temperature","humidity","ph","rainfall","label"]).to_csv(OUT, index=False)
print(f"Wrote {len(rows)} synthetic demo rows to {OUT}")
