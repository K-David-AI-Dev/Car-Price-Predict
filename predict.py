import warnings
import os
import joblib
import pandas as pd
import numpy as np

# Figyelmeztetések kikapcsolása
warnings.filterwarnings("ignore", category=UserWarning)

def run_predictor():
    try:
        # Modell betöltése
        data = joblib.load('car_price_full_pipeline.pkl')
        pipeline = data['pipeline']
        brand_mapping = data['brand_mapping']
        model_mapping = data['model_mapping']
        km_mean = data['km_mean']
        feature_names = data['feature_names']
    except FileNotFoundError:
        print("\nHiba: A 'car_price_full_pipeline.pkl' nem található a mappában!")
        return

    print("\n" + "="*40)
    print("      CAR PRICE ESTIMATOR INTERFACE")
    print("="*40)
    
    # 1. MÁRKA ELLENŐRZÉSE
    brand = input("\n1. Brand (e.g., Toyota): ").strip().title()
    if brand in brand_mapping:
        print(f"   [OK] {brand} is in the database.")
        brand_val = brand_mapping[brand]
    else:
        print(f"   [!] {brand} not found. Using average price.")
        brand_val = np.mean(list(brand_mapping.values()))

    # 2. MODELL ELLENŐRZÉSE
    model = input("2. Model (e.g., Yaris): ").strip().title()
    if model in model_mapping:
        print(f"   [OK] {model} is in the database.")
        model_val = model_mapping[model]
    else:
        print(f"   [!] {model} not found. Using global average.")
        model_val = np.mean(list(model_mapping.values()))

    # 3. EGYÉB ADATOK
    try:
        year = int(input("3. Year of manufacture: "))
    except: year = 2015

    try:
        km_input = input(f"4. Kilometers (Enter for avg: {int(km_mean)}): ")
        km = float(km_input) if km_input else km_mean
    except: km = km_mean

    fuel = input("5. Fuel Type (Diesel/Petrol/Hybrid): ").strip().title()
    trans = input("6. Transmission (Manual/Automatic): ").strip().title()
    owner = input("7. Owner (First/Second): ").strip().lower()

    # ADATFELDOLGOZÁS
    input_df = pd.DataFrame(0, index=[0], columns=feature_names)
    input_df['Year'] = year
    input_df['Age'] = 2026 - year
    input_df['kmDriven'] = km
    input_df['Brand_encoded'] = brand_val
    input_df['model_encoded'] = model_val

    if f'FuelType_{fuel}' in input_df.columns: input_df[f'FuelType_{fuel}'] = 1
    if f'Transmission_{trans}' in input_df.columns: input_df[f'Transmission_{trans}'] = 1
    if f'Owner_{owner}' in input_df.columns: input_df[f'Owner_{owner}'] = 1

    # BECSLÉS
    prediction = pipeline.predict(input_df)[0]
    print("\n" + "*"*40)
    print(f" ESTIMATED PRICE: {prediction:.2f} EUR")
    print("*"*40)

if __name__ == "__main__":
    while True:
        run_predictor()
        if input("\nEstimate another car? (y/n): ").lower() != 'y':
            break