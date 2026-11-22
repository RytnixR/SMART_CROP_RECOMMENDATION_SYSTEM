# SMART CROP RECOMMENDATION SYSTEM

Capstone project: a crop recommendation prototype using soil nutrients and weather conditions.

## Project features
- Inputs: Nitrogen (N), Phosphorus (P), Potassium (K), temperature, humidity, soil pH and rainfall.
- Data validation and preprocessing.
- Decision Tree and Random Forest model comparison.
- Crop prediction with model confidence when supported.
- Evaluation metrics: accuracy, precision, recall and F1-score.
- SQLite prediction history and CSV export.

## Run on Windows (PowerShell)
Open the project root folder in VS Code. Keep the backend and frontend running in separate terminals.

### Terminal 1 — Backend
```powershell
.\start_backend.ps1
```
The API will be available at http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

### Terminal 2 — Frontend
```powershell
.\start_frontend.ps1
```
Open http://localhost:5173. The Vite development server proxies `/api` requests to FastAPI at port 8000.

## Manual start (alternative)
From the project root, ensure the root `.venv` exists and is activated, then run:
```powershell
cd .\backend
pip install -r requirements.txt
python generate_demo_data.py
python train_model.py
python -m uvicorn app.main:app --reload
```
In a second terminal:
```powershell
cd .\frontend
npm install
npm run dev
```

## Dataset note
The included `generate_demo_data.py` creates synthetic data only for testing the software flow. These generated records are not verified agronomic data and must not be presented as real-world agricultural evidence. Replace `backend/data/crop_recommendation.csv` with a suitable verified dataset before interpreting model metrics or using recommendations outside a demonstration. The prototype is decision support, not a replacement for local soil testing or agricultural expertise.

## CSV format
Use these exact columns: `N,P,K,temperature,humidity,ph,rainfall,label`. After replacing the dataset, run `python train_model.py` again from the `backend` folder.
