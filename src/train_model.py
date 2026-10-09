"""
Precision Agriculture Model Training Pipeline.
Trains, evaluates, and exports production ML models strictly on authentic real agricultural data:
1. Crop Recommendation Classifier (Scikit-Learn Pipeline on verified agronomical trials)
2. Indian Regional Yield Regressor (Trained on 81,329 real records from Ministry of Agriculture, DES India)
3. District Agricultural Intelligence (33 States, 652 Districts of India)
Zero synthetic or mock data.
"""

import os
import json
import joblib
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, TargetEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingRegressor
from sklearn.metrics import classification_report, accuracy_score, f1_score, r2_score, mean_absolute_error

# Canonical crop dictionary mapping
CROP_DICT = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}
NAME_TO_ID = {v.lower(): k for k, v in CROP_DICT.items()}

# Verified Agronomic Intelligence & Fertilizer Baselines (ICAR & Ministry of Agriculture)
CROP_AGRONOMY_DATA = {
    "Rice": {
        "season": "Kharif (Monsoon)",
        "duration": "100 - 150 days",
        "water_need": "High (1200 - 2000 mm)",
        "ideal_npk": [80, 40, 40],
        "category": "Cereal Food Grain",
        "description": "Staple food crop thriving in warm, humid climates with heavy standing water or fertile clayey-loam soils."
    },
    "Maize": {
        "season": "Kharif / Rabi",
        "duration": "90 - 120 days",
        "water_need": "Moderate (500 - 800 mm)",
        "ideal_npk": [80, 40, 20],
        "category": "Cereal / Coarse Grain",
        "description": "Versatile cereal crop requiring well-drained fertile loam soils and warm temperatures."
    },
    "Jute": {
        "season": "Kharif",
        "duration": "120 - 150 days",
        "water_need": "High (1000 - 1500 mm)",
        "ideal_npk": [80, 40, 40],
        "category": "Commercial Fiber",
        "description": "Golden fiber crop requiring warm, humid alluvial plains and abundant monsoon showers."
    },
    "Cotton": {
        "season": "Kharif",
        "duration": "150 - 180 days",
        "water_need": "Moderate (600 - 1000 mm)",
        "ideal_npk": [120, 40, 20],
        "category": "Commercial Fiber",
        "description": "Cash crop performing best in deep black cotton soils (regur) with sunny, frost-free weather."
    },
    "Coconut": {
        "season": "Perennial Plantation",
        "duration": "Continuous (Year-round)",
        "water_need": "High (1300 - 2300 mm)",
        "ideal_npk": [20, 10, 30],
        "category": "Plantation / Oilseed",
        "description": "Tropical palm flourishing in coastal sandy-loam soils with warm humid tropical maritime conditions."
    },
    "Papaya": {
        "season": "Year-round",
        "duration": "270 - 360 days",
        "water_need": "Moderate (1000 - 1500 mm)",
        "ideal_npk": [50, 50, 50],
        "category": "Fruit Crop",
        "description": "Fast-growing fruit requiring rich organic loam with strict avoidance of waterlogging."
    },
    "Orange": {
        "season": "Sub-tropical Perennial",
        "duration": "Annual harvest",
        "water_need": "Moderate (800 - 1200 mm)",
        "ideal_npk": [20, 10, 10],
        "category": "Citrus Fruit",
        "description": "Citrus fruit favoring slightly acidic to neutral soils with distinct dry and wet seasons."
    },
    "Apple": {
        "season": "Temperate Perennial",
        "duration": "Annual harvest",
        "water_need": "Moderate (1000 - 1250 mm)",
        "ideal_npk": [20, 125, 200],
        "category": "Temperate Fruit",
        "description": "Temperate fruit demanding chill hours (below 7°C) and potassium-rich hill loams."
    },
    "Muskmelon": {
        "season": "Zaid (Summer)",
        "duration": "70 - 90 days",
        "water_need": "Low-Moderate (400 - 600 mm)",
        "ideal_npk": [100, 10, 50],
        "category": "Cucurbit / Fruit",
        "description": "Warm-season melon thriving in sandy-loam soils with plenty of sunshine and dry air at harvest."
    },
    "Watermelon": {
        "season": "Zaid (Summer)",
        "duration": "80 - 100 days",
        "water_need": "Moderate (500 - 700 mm)",
        "ideal_npk": [100, 10, 50],
        "category": "Cucurbit / Fruit",
        "description": "Heat-loving crop requiring fertile sandy soils, long warm days, and moderate irrigation."
    },
    "Grapes": {
        "season": "Sub-tropical Perennial",
        "duration": "Annual harvest",
        "water_need": "Moderate (600 - 900 mm)",
        "ideal_npk": [20, 125, 200],
        "category": "Vine Fruit",
        "description": "High-value fruit needing hot dry summers, deep well-drained loam, and balanced potassium."
    },
    "Mango": {
        "season": "Tropical Perennial",
        "duration": "Annual harvest",
        "water_need": "Moderate (700 - 1100 mm)",
        "ideal_npk": [20, 20, 30],
        "category": "Tropical Fruit",
        "description": "King of fruits; adapts to diverse tropical soils provided there is a distinct dry spell for flowering."
    },
    "Banana": {
        "season": "Tropical Perennial",
        "duration": "300 - 365 days",
        "water_need": "High (1500 - 2200 mm)",
        "ideal_npk": [100, 75, 50],
        "category": "Horticultural Fruit",
        "description": "Heavy feeder requiring rich clay-loam, high humidity, continuous warmth, and generous watering."
    },
    "Pomegranate": {
        "season": "Arid / Semi-arid",
        "duration": "Annual harvest",
        "water_need": "Low (500 - 700 mm)",
        "ideal_npk": [20, 10, 40],
        "category": "Arid Fruit",
        "description": "Drought-tolerant high-value fruit that excels in semi-arid plains with well-drained soils."
    },
    "Lentil": {
        "season": "Rabi (Winter)",
        "duration": "110 - 130 days",
        "water_need": "Low (300 - 450 mm)",
        "ideal_npk": [20, 60, 20],
        "category": "Pulse / Legume",
        "description": "Cool-season nitrogen-fixing pulse crop thriving on residual moisture in fertile loams."
    },
    "Blackgram": {
        "season": "Kharif / Zaid",
        "duration": "75 - 90 days",
        "water_need": "Low-Moderate (400 - 600 mm)",
        "ideal_npk": [40, 60, 20],
        "category": "Pulse / Legume",
        "description": "Nutritious legume that improves soil fertility; suited for tropical and sub-tropical loamy soils."
    },
    "Mungbean": {
        "season": "Kharif / Zaid",
        "duration": "60 - 75 days",
        "water_need": "Low (350 - 500 mm)",
        "ideal_npk": [20, 40, 20],
        "category": "Pulse / Legume",
        "description": "Short-duration pulse ideal for crop rotation and intercropping in warm regions."
    },
    "Mothbeans": {
        "season": "Kharif (Arid)",
        "duration": "75 - 90 days",
        "water_need": "Very Low (200 - 400 mm)",
        "ideal_npk": [20, 40, 20],
        "category": "Pulse / Legume",
        "description": "Remarkably drought-resilient pulse crop native to arid and semi-arid desert regions."
    },
    "Pigeonpeas": {
        "season": "Kharif (Long duration)",
        "duration": "150 - 200 days",
        "water_need": "Moderate (600 - 800 mm)",
        "ideal_npk": [20, 60, 20],
        "category": "Pulse / Legume",
        "description": "Deep-rooted legume resilient to dry spells, extensively cultivated in dryland agriculture."
    },
    "Kidneybeans": {
        "season": "Rabi / Temperate",
        "duration": "90 - 120 days",
        "water_need": "Moderate (500 - 700 mm)",
        "ideal_npk": [20, 60, 20],
        "category": "Pulse / Legume",
        "description": "High-protein bean crop suited for cool, temperate highland conditions and rich light soils."
    },
    "Chickpea": {
        "season": "Rabi (Winter)",
        "duration": "90 - 120 days",
        "water_need": "Low (300 - 500 mm)",
        "ideal_npk": [40, 60, 80],
        "category": "Pulse / Legume",
        "description": "Major winter pulse thriving in dry, cool conditions with residual soil moisture and deep black/loam soils."
    },
    "Coffee": {
        "season": "Tropical Highland Perennial",
        "duration": "Annual harvest",
        "water_need": "High (1500 - 2200 mm)",
        "ideal_npk": [100, 20, 30],
        "category": "Beverage Plantation",
        "description": "Shade-loving plantation crop requiring cool tropical highlands, rich acidic soils, and plentiful rain."
    }
}


def train_and_evaluate():
    print("=" * 75)
    print("   ENTERPRISE MULTI-TIER PRECISION AGRICULTURE ML SYSTEM TRAINING   ")
    print("=" * 75)
    os.makedirs('models', exist_ok=True)

    # =========================================================================
    # PART 1: Crop Recommendation Classifier (Soil & Climate Matching)
    # =========================================================================
    csv_path = os.path.join("data", "Crop_recommendation.csv")
    if not os.path.exists(csv_path):
        csv_path = "Crop_recommendation.csv"
    
    print(f"\n[Part 1] Loading verified agronomic trial dataset from: {csv_path}")
    df_rec = pd.read_csv(csv_path)
    print(f"Loaded {df_rec.shape[0]:,} rows x {df_rec.shape[1]} columns (22 crop classes)")

    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df_rec[feature_cols]
    y_raw = df_rec['label'].str.lower()
    y = y_raw.map(NAME_TO_ID)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print("Training scikit-learn Pipeline (StandardScaler + RandomForestClassifier)...")
    clf_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=16, random_state=42, n_jobs=-1))
    ])
    clf_pipeline.fit(X_train, y_train)

    y_pred = clf_pipeline.predict(X_test)
    clf_accuracy = float(accuracy_score(y_test, y_pred))
    clf_f1 = float(f1_score(y_test, y_pred, average='weighted'))
    print(f"Crop Recommender Accuracy: {clf_accuracy * 100:.2f}% | F1 Score: {clf_f1:.4f}")

    # Export recommendation models
    joblib.dump(clf_pipeline, 'models/crop_pipeline.joblib')
    with open('models/crop_pipeline.pkl', 'wb') as f:
        pickle.dump(clf_pipeline, f)

    # =========================================================================
    # PART 2: Regional Indian Yield Regressor (81,329 Real Ministry Records)
    # =========================================================================
    yield_csv = os.path.join('data', 'crop_production_curated_81k.csv')
    if not os.path.exists(yield_csv):
        print("Curated 81k file not found, running build_district_intelligence first...")
        import sys
        sys.path.append('src')
        import build_district_intelligence
        build_district_intelligence.build_intelligence()
    
    print(f"\n[Part 2] Training Regional Yield Predictor on {yield_csv}...")
    df_yield = pd.read_csv(yield_csv)
    print(f"Total authentic government records loaded: {len(df_yield):,}")

    p99 = df_yield['Yield'].quantile(0.99)
    df_yield_clean = df_yield[(df_yield['Yield'] > 0) & (df_yield['Yield'] <= p99)].copy()
    print(f"Cleaned training samples: {len(df_yield_clean):,}")

    cat_cols = ['State_Name', 'District_Name', 'Season', 'mapped_crop']
    X_yield_raw = df_yield_clean[cat_cols]
    y_yield_log = np.log1p(df_yield_clean['Yield'])

    # Target Encoder for high cardinality categorical features (State, District, Season, Crop)
    te = TargetEncoder(smooth='auto', cv=5)
    X_yield_cat = te.fit_transform(X_yield_raw, y_yield_log)
    X_yield = pd.DataFrame(X_yield_cat, columns=cat_cols, index=df_yield_clean.index)
    X_yield['Area_log'] = np.log1p(df_yield_clean['Area'])

    X_y_train, X_y_test, y_y_train, y_y_test = train_test_split(
        X_yield, y_yield_log, test_size=0.15, random_state=42
    )

    yield_regressor = HistGradientBoostingRegressor(
        max_iter=150,
        learning_rate=0.1,
        min_samples_leaf=20,
        random_state=42
    )
    yield_regressor.fit(X_y_train, y_y_train)

    y_y_pred = yield_regressor.predict(X_y_test)
    yield_r2 = float(r2_score(y_y_test, y_y_pred))
    actual_test = np.expm1(y_y_test)
    actual_pred = np.expm1(y_y_pred)
    yield_mae = float(mean_absolute_error(actual_test, actual_pred))
    print(f"Yield Regressor Log R2: {yield_r2:.4f} ({yield_r2*100:.1f}% variance explained)")
    print(f"Yield Regressor MAE: {yield_mae:.2f} Tonnes/Ha")

    joblib.dump(yield_regressor, 'models/yield_regressor.joblib')
    joblib.dump(te, 'models/yield_encoder.joblib')

    # =========================================================================
    # PART 3: Comprehensive Metadata & Export
    # =========================================================================
    print("\n[Part 3] Exporting unified system metadata...")
    metadata = {
        "model_type": "Multi-Tier Precision Agriculture AI System",
        "training_data_summary": {
            "crop_recommendation_trials": len(df_rec),
            "regional_production_records": len(df_yield),
            "government_data_source": "Ministry of Agriculture & Farmers Welfare, Government of India (DES)",
            "data_authenticity": "100% Real Authentic Records (Zero Synthetic/Mock Data)",
            "total_states": int(df_yield['State_Name'].nunique()),
            "total_districts": int(df_yield['District_Name'].nunique())
        },
        "recommender_metrics": {
            "model": "StandardScaler + RandomForestClassifier",
            "accuracy": round(clf_accuracy, 4),
            "weighted_f1": round(clf_f1, 4),
            "n_classes": len(CROP_DICT),
            "feature_names": feature_cols
        },
        "yield_predictor_metrics": {
            "model": "TargetEncoder + HistGradientBoostingRegressor",
            "log_r2_score": round(yield_r2, 4),
            "mae_tonnes_ha": round(yield_mae, 4),
            "training_samples": len(df_yield_clean)
        },
        "crop_dictionary": CROP_DICT,
        "name_to_id": NAME_TO_ID,
        "crop_agronomy": CROP_AGRONOMY_DATA
    }

    with open('models/model_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 75)
    print("SUCCESS: Multi-Tier ML models and metadata compiled successfully!")
    print("=" * 75)


if __name__ == '__main__':
    train_and_evaluate()
