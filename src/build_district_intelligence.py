"""
Build District Crop Intelligence Database from Real Ministry of Agriculture Data.
Processes 242,000+ real records to create district-level crop rankings, historical yields,
and ICAR / Soil Health Card agro-climatic benchmarks.
"""

import json
import os
import pandas as pd
import numpy as np

# Typical State-level Agro-Ecological and Soil Health Card Norms
# Based on ICAR NBSS&LUP and DAC&FW Soil Health Card National Portal
STATE_SOIL_BENCHMARKS = {
    'Gujarat': {
        'soil_type': 'Alluvial Sandy-Loam / Medium Black',
        'N': 195, 'P': 26, 'K': 285, 'ph': 7.5,
        'rainfall_normal': 820.0, 'temp_normal': 27.5, 'humidity_normal': 64.0
    },
    'Maharashtra': {
        'soil_type': 'Medium to Deep Black Cotton (Regur)',
        'N': 180, 'P': 20, 'K': 310, 'ph': 7.6,
        'rainfall_normal': 1050.0, 'temp_normal': 26.8, 'humidity_normal': 68.0
    },
    'Punjab': {
        'soil_type': 'Indo-Gangetic Alluvial Loam',
        'N': 240, 'P': 28, 'K': 220, 'ph': 7.8,
        'rainfall_normal': 650.0, 'temp_normal': 24.2, 'humidity_normal': 62.0
    },
    'Haryana': {
        'soil_type': 'Alluvial / Sierozem Loamy Sand',
        'N': 210, 'P': 24, 'K': 230, 'ph': 7.9,
        'rainfall_normal': 580.0, 'temp_normal': 25.0, 'humidity_normal': 60.0
    },
    'Uttar Pradesh': {
        'soil_type': 'Gangetic Alluvial Silt-Loam',
        'N': 215, 'P': 22, 'K': 210, 'ph': 7.3,
        'rainfall_normal': 950.0, 'temp_normal': 25.6, 'humidity_normal': 66.0
    },
    'Madhya Pradesh': {
        'soil_type': 'Mixed Red and Black Soil',
        'N': 175, 'P': 18, 'K': 260, 'ph': 7.2,
        'rainfall_normal': 1020.0, 'temp_normal': 26.2, 'humidity_normal': 61.0
    },
    'Karnataka': {
        'soil_type': 'Red Sandy Loam / Deep Black',
        'N': 190, 'P': 25, 'K': 240, 'ph': 6.8,
        'rainfall_normal': 1180.0, 'temp_normal': 25.5, 'humidity_normal': 72.0
    },
    'Tamil Nadu': {
        'soil_type': 'Red Loam / Coastal Alluvial',
        'N': 205, 'P': 23, 'K': 250, 'ph': 6.9,
        'rainfall_normal': 960.0, 'temp_normal': 28.5, 'humidity_normal': 74.0
    },
    'Andhra Pradesh': {
        'soil_type': 'Red Sandy Clay / Coastal Alluvium',
        'N': 195, 'P': 27, 'K': 270, 'ph': 7.1,
        'rainfall_normal': 920.0, 'temp_normal': 28.0, 'humidity_normal': 71.0
    },
    'Telangana': {
        'soil_type': 'Red Earth (Chalka) / Black Cotton',
        'N': 185, 'P': 22, 'K': 265, 'ph': 7.3,
        'rainfall_normal': 910.0, 'temp_normal': 27.8, 'humidity_normal': 66.0
    },
    'Rajasthan': {
        'soil_type': 'Arid Desert Sandy / Grey Brown Alluvial',
        'N': 140, 'P': 16, 'K': 290, 'ph': 8.1,
        'rainfall_normal': 460.0, 'temp_normal': 27.0, 'humidity_normal': 52.0
    },
    'West Bengal': {
        'soil_type': 'Deltaic Alluvial Silt Loam',
        'N': 250, 'P': 24, 'K': 190, 'ph': 6.2,
        'rainfall_normal': 1650.0, 'temp_normal': 26.5, 'humidity_normal': 79.0
    },
    'Bihar': {
        'soil_type': 'North Gangetic Calcareous Alluvial',
        'N': 210, 'P': 20, 'K': 200, 'ph': 7.4,
        'rainfall_normal': 1120.0, 'temp_normal': 25.8, 'humidity_normal': 70.0
    },
    'Kerala': {
        'soil_type': 'Laterite / Coastal Alluvial Acidic',
        'N': 220, 'P': 19, 'K': 170, 'ph': 5.4,
        'rainfall_normal': 2850.0, 'temp_normal': 27.2, 'humidity_normal': 83.0
    },
    'Assam': {
        'soil_type': 'Brahmaputra River Alluvial & Acidic',
        'N': 240, 'P': 18, 'K': 160, 'ph': 5.2,
        'rainfall_normal': 2400.0, 'temp_normal': 24.5, 'humidity_normal': 82.0
    },
    'Odisha': {
        'soil_type': 'Red & Yellow / Coastal Saline Alluvium',
        'N': 190, 'P': 18, 'K': 210, 'ph': 6.3,
        'rainfall_normal': 1450.0, 'temp_normal': 27.0, 'humidity_normal': 76.0
    },
    'Himachal Pradesh': {
        'soil_type': 'Mountain Brown Forest Loam',
        'N': 230, 'P': 22, 'K': 240, 'ph': 6.5,
        'rainfall_normal': 1250.0, 'temp_normal': 18.0, 'humidity_normal': 65.0
    },
    'Jammu and Kashmir': {
        'soil_type': 'Sub-Montane Alluvial & Karewa Loam',
        'N': 220, 'P': 21, 'K': 230, 'ph': 6.8,
        'rainfall_normal': 980.0, 'temp_normal': 16.5, 'humidity_normal': 64.0
    },
    'Uttarakhand': {
        'soil_type': 'Tarai Alluvial / Bhabar Loam',
        'N': 235, 'P': 24, 'K': 215, 'ph': 6.6,
        'rainfall_normal': 1520.0, 'temp_normal': 21.0, 'humidity_normal': 70.0
    },
    'Jharkhand': {
        'soil_type': 'Red Sandy Clay Lateritic',
        'N': 180, 'P': 17, 'K': 210, 'ph': 5.8,
        'rainfall_normal': 1280.0, 'temp_normal': 25.5, 'humidity_normal': 69.0
    },
    'Chhattisgarh': {
        'soil_type': 'Red and Yellow (Matasi) / Black (Kanhar)',
        'N': 185, 'P': 18, 'K': 225, 'ph': 6.5,
        'rainfall_normal': 1360.0, 'temp_normal': 26.5, 'humidity_normal': 68.0
    }
}

DEFAULT_BENCHMARK = {
    'soil_type': 'Fertile Loam / Agricultural Alluvium',
    'N': 200, 'P': 22, 'K': 230, 'ph': 7.0,
    'rainfall_normal': 1000.0, 'temp_normal': 26.0, 'humidity_normal': 65.0
}

CROP_MAPPING = {
    'Rice': 'rice', 'Paddy': 'rice',
    'Maize': 'maize',
    'Gram': 'chickpea',
    'Arhar/Tur': 'pigeonpeas',
    'Moong(Green Gram)': 'mungbean',
    'Urad': 'blackgram', 'Blackgram': 'blackgram',
    'Masoor': 'lentil', 'Lentil': 'lentil',
    'Pome Granet': 'pomegranate',
    'Banana': 'banana',
    'Mango': 'mango',
    'Grapes': 'grapes',
    'Water Melon': 'watermelon',
    'Apple': 'apple',
    'Orange': 'orange',
    'Papaya': 'papaya',
    'Coconut ': 'coconut', 'Coconut': 'coconut',
    'Cotton(lint)': 'cotton',
    'Jute': 'jute', 'Jute & mesta': 'jute',
    'Coffee': 'coffee',
    'Moth': 'mothbeans'
}

def build_intelligence():
    raw_path = os.path.join('data', 'crop_production.csv')
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Missing {raw_path}")
    
    print("Reading crop_production.csv...")
    df = pd.read_csv(raw_path).dropna(subset=['Production', 'Area'])
    df['State_Name'] = df['State_Name'].str.strip()
    df['District_Name'] = df['District_Name'].str.strip()
    df['Season'] = df['Season'].str.strip()
    df['Crop'] = df['Crop'].str.strip()
    df['Yield'] = (df['Production'] / df['Area']).round(2)
    
    # Filter reasonable positive areas
    df = df[(df['Area'] > 0) & (df['Production'] > 0)]
    
    states = sorted(df['State_Name'].unique())
    districts_by_state = {}
    district_data = {}
    crop_district_map = {}
    
    for state in states:
        state_df = df[df['State_Name'] == state]
        districts = sorted(state_df['District_Name'].unique())
        districts_by_state[state] = districts
        
        state_benchmark = STATE_SOIL_BENCHMARKS.get(state, DEFAULT_BENCHMARK)
        
        for dist in districts:
            dist_df = state_df[state_df['District_Name'] == dist]
            
            # Aggregate top crops in this district
            crop_groups = dist_df.groupby('Crop')
            crop_stats = []
            
            for crop_name, grp in crop_groups:
                count = len(grp)
                avg_yield = float(grp['Yield'].median())
                if np.isnan(avg_yield) or avg_yield <= 0:
                    avg_yield = float(grp['Yield'].mean())
                avg_yield = round(avg_yield, 2)
                
                # Primary season
                season_counts = grp['Season'].value_counts()
                primary_season = season_counts.index[0] if len(season_counts) > 0 else 'Kharif'
                
                mapped = CROP_MAPPING.get(crop_name, crop_name.lower())
                
                crop_stats.append({
                    'crop': crop_name,
                    'mapped_crop': mapped,
                    'records_count': int(count),
                    'avg_yield_tonnes_ha': float(avg_yield),
                    'primary_season': primary_season,
                    'is_recommendation_crop': mapped in CROP_MAPPING.values()
                })
                
                # Also track crop_district_map
                if mapped not in crop_district_map:
                    crop_district_map[mapped] = []
                crop_district_map[mapped].append({
                    'state': state,
                    'district': dist,
                    'records': int(count),
                    'avg_yield': float(avg_yield)
                })
            
            # Sort top crops by count (frequency of cultivation over years)
            crop_stats.sort(key=lambda x: x['records_count'], reverse=True)
            
            # District specific benchmark
            dist_key = f"{state}::{dist}"
            district_data[dist_key] = {
                'state': state,
                'district': dist,
                'total_records': len(dist_df),
                'top_crops': crop_stats[:12],  # top 12 cultivated crops
                'soil_benchmark': state_benchmark
            }
    
    # Sort top districts for each crop
    for c in crop_district_map:
        crop_district_map[c].sort(key=lambda x: x['records'], reverse=True)
        crop_district_map[c] = crop_district_map[c][:15] # top 15 districts in India
    
    output = {
        'total_records_processed': len(df),
        'total_states': len(states),
        'total_districts': sum(len(d) for d in districts_by_state.values()),
        'states': states,
        'districts_by_state': districts_by_state,
        'district_data': district_data,
        'crop_top_districts': crop_district_map,
        'state_benchmarks': STATE_SOIL_BENCHMARKS
    }
    
    out_path = os.path.join('models', 'district_crop_intelligence.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    file_size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"Intelligence successfully written to {out_path} ({file_size_mb:.2f} MB)")
    print(f"Covering {len(states)} States and {len(district_data)} Districts!")

if __name__ == '__main__':
    build_intelligence()
