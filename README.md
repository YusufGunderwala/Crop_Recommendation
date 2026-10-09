# 🌾 Crop Recommendation & Soil Health Advisory System

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.1-emerald.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Model-Random%20Forest%20Classifier-orange.svg)](https://scikit-learn.org/)
[![Dataset](https://img.shields.io/badge/Dataset-2%2C200%20Real%20Records-green.svg)](data/Crop_recommendation.csv)
[![Holdout Accuracy](https://img.shields.io/badge/Accuracy-99.77%25-brightgreen.svg)]()

> An end-to-end Machine Learning web application and REST API that recommends optimal agricultural crops based on field soil test measurements and local climate parameters, featuring an integrated **Chemical Fertilizer Prescription Engine**, **Live Weather Telemetry**, and **Interactive Nutrient Radar Analytics**. Trained strictly on 100% real, authentic agricultural records. Zero mock or synthetic data.

---

## 📌 Table of Contents
1. [Key Highlights](#-key-highlights)
2. [Authentic Dataset (2,200 Verified Records)](#-authentic-dataset-2200-verified-records)
3. [Machine Learning Pipeline](#-machine-learning-pipeline)
4. [Scientific Input Separation](#-scientific-input-separation)
5. [API Documentation (`/api/predict`)](#-api-documentation-apipredict)
6. [Directory Structure](#-directory-structure)
7. [Installation & Run Guide](#-installation--run-guide)

---

## 🚀 Key Highlights

- **100% Real Benchmark Data:** Trained strictly on 2,200 verified real field records across 22 crops (100 balanced samples per crop). Zero mock or artificially synthesized data.
- **Fixed Scaler Mismatch Bug:** Encapsulates preprocessing and classifier inside a single scikit-learn `Pipeline([('scaler', StandardScaler()), ('classifier', RandomForestClassifier())])`, permanently eliminating inference distortion.
- **Top-3 Calibrated Recommendations:** Outputs ranked top-3 alternative crops with calibrated probability match scores.
- **Precision Fertilizer & Soil Health Advisory:** Automatically computes chemical nutrient gaps ($\Delta N, \Delta P, \Delta K$) against optimal agronomical thresholds and prescribes exact dosages of **Urea (46% N)**, **DAP (46% P2O5)**, and **MOP / Potash (60% K2O)**.
- **Live Weather Station Telemetry:** Integrates Open-Meteo weather station telemetry to query real-time Temperature (°C), Humidity (%), and Precipitation (mm) for any city or GPS coordinates.
- **Visual Analytics with Chart.js:**
  - **Soil Nutrient Radar Chart:** Contrasts farmer's soil test profile directly against the recommended crop's ideal target.
- **Clean, Professional UI:** Minimalist SaaS dashboard without tacky AI badges or marketing buzzwords.

---

## 📊 Authentic Dataset (2,200 Verified Records)

The model is trained on the authentic precision agriculture benchmark dataset ([data/Crop_recommendation.csv](data/Crop_recommendation.csv)), containing 2,200 observations with 100 balanced instances for each of the 22 crops:

| Feature | Agronomical Meaning | Unit |
| :--- | :--- | :--- |
| **N** | Nitrogen content in soil | kg/ha |
| **P** | Phosphorus content in soil | kg/ha |
| **K** | Potassium content in soil | kg/ha |
| **pH** | Soil acidity / alkalinity | 0 – 14 scale |
| **Temperature** | Ambient temperature | °C |
| **Humidity** | Relative air humidity | % |
| **Rainfall** | Precipitation | mm |

**Target Crops (22 Classes):** Rice, Maize, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee.

---

## 🔬 Machine Learning Pipeline

- **Algorithm:** Tuned `RandomForestClassifier(n_estimators=100, random_state=42)`
- **Evaluation Split:** 80% Train (1,760 samples), 20% Holdout Test (440 samples) with exact class stratification.
- **Holdout Test Accuracy:** **99.77%**
- **Holdout Test F1-Score:** **0.9977**

### Feature Importance Weights:
- **Rainfall:** 23.33%
- **Relative Humidity:** 21.74%
- **Potassium (K):** 17.27%
- **Phosphorus (P):** 15.31%
- **Nitrogen (N):** 9.73%
- **Temperature:** 7.42%
- **Soil pH:** 5.20%

---

## 🌿 Scientific Input Separation

1. **Soil Chemistry ($N, P, K$, and pH):** Resides in the ground and must be entered from the user's **Soil Health Card (मृदा स्वास्थ्य कार्ड)** or lab testing report. No GPS can measure underground soil chemistry.
2. **Atmospheric Climate (Temperature, Humidity, Rainfall):** Can be fetched live from real weather stations using the device GPS or city search, or entered manually.

---

## 🔌 API Documentation (`/api/predict`)

### Endpoint: `POST /api/predict`
**Request Headers:** `Content-Type: application/json`

**Sample Request Body:**
```json
{
  "N": 90.0,
  "P": 42.0,
  "K": 43.0,
  "ph": 6.5,
  "temperature": 20.88,
  "humidity": 82.0,
  "rainfall": 202.94
}
```

**Sample Response Body:**
```json
{
  "status": "success",
  "data": {
    "primary_crop": "Rice",
    "primary_confidence": 98.0,
    "top_predictions": [
      {
        "rank": 1,
        "crop": "Rice",
        "confidence": 98.0,
        "season": "Kharif (Monsoon)",
        "duration": "100 - 150 days",
        "water_need": "High (1200 - 2000 mm)",
        "category": "Cereal Food Grain"
      }
    ],
    "advisory": {
      "ph_status": "Optimal / Neutral",
      "ph_advice": "Soil pH is in the ideal neutral buffer range (6.0 - 7.5)...",
      "recommendations": [
        {
          "nutrient": "Nitrogen (N)",
          "status": "Optimal",
          "gap": "Balanced",
          "action": "Soil nitrogen level is optimal for this crop."
        }
      ]
    }
  },
  "model": "RandomForestClassifier",
  "dataset_rows": 2200
}
```

---

## 📂 Directory Structure

```
Crop_Recommendation/
├── app.py                             # Clean Flask server & REST API
├── requirements.txt                   # Production dependencies
├── README.md                          # Documentation
├── Crop Recommendation Using Machine Learning.ipynb # Model research notebook
├── data/
│   ├── Crop_recommendation.csv        # Authentic 2,200 agronomic trial records
│   ├── crop_production.csv            # Ministry of Agriculture historical records
│   └── crop_production_curated_81k.csv # Curated 81,329 district records
├── models/
│   ├── crop_pipeline.joblib           # Production scikit-learn Pipeline
│   ├── crop_pipeline.pkl              # Production pipeline (pickle format)
│   ├── district_coords_cache.json     # 652 district coordinates cache (0ms latency)
│   ├── district_crop_intelligence.json# Historical crop profiles by district
│   ├── model_metadata.json            # Model metrics and agronomy rules
│   ├── yield_encoder.joblib           # TargetEncoder for district yield
│   └── yield_regressor.joblib         # Gradient boosting yield regressor
├── src/
│   ├── train_model.py                 # Multi-task ML training pipeline
│   └── build_district_intelligence.py # District analytics builder
├── static/
│   ├── annie-spratt-e6AxXcUSeig-unsplash.jpg # Clean background image
│   └── crop.png                       # Project logo
└── templates/
    └── index.html                     # Precision Agronomy SaaS dashboard
```

---

## ⚡ Installation & Run Guide

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Retrain model on real dataset
python src/train_model.py

# 3. Start web server
python app.py
```
Open browser at: `http://127.0.0.1:5000`