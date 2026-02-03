import os
import sys

print("--- Rendszerellenőrzés ---")
print(f"Python verzió: {sys.version}")
print(f"Jelenlegi mappa: {os.getcwd()}")

files_in_folder = os.listdir()
print(f"Fájlok a mappában: {files_in_folder}")

if 'car_price_full_pipeline.pkl' in files_in_folder:
    print("✅ A modellfájl MEGVAN!")
else:
    print("❌ A 'car_price_full_pipeline.pkl' HIÁNYZIK ebből a mappából!")

if 'predict.py' in files_in_folder:
    print("✅ A predict.py MEGVAN!")
else:
    print("❌ A 'predict.py' HIÁNYZIK!")