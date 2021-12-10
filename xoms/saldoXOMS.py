#Bajar el .csv de XOMS
# Tomar columna "disponible p garantias mtr E"
# Tomar colum D 
# Hacer el val absoluto de ambas celdas D y E, y tmar el mayor
# Abrir saldobot.xls y ver el saldo para esa cuenta
# A saldo le resto el val absoluto

# hacer json

##IMPORTS
from argparse import ArgumentParser
import csv
import os, glob, sys
import pandas as pd
from pathlib import Path

def load_files():
    EXTENSIONS_ALLOWED = ['*.xls','*.xlsx','*.csv']
    files_grabbed = []
    for files in EXTENSIONS_ALLOWED:
        files_grabbed.extend(glob.glob(files))
    return files_grabbed
def select_file(files, keyword):
    for f in files:
        if keyword in f:
            return f
    return None
def process(file,file2):
    if (not file) or (not file2):
        return "File not found"
    df1 = pd.read_excel(file)) #XOMS
    df2 = pd.read_excel(file2) #BOTS
    df1["abs_max"] = df1[["Disponible p/Garantías Opciones Byma", "Disponible p/Garantías MtR"]].max(axis=1)
    mergedStuff = pd.merge(df, df2, on=['Producto'], how='inner')
    #Sumamos por comitenente y moneda
    df_diferencias = mergedStuff.groupby(['Comitente','Moneda de liquidación '],as_index=False)[['Dif. Día']].sum()
    return df_diferencias



account = "XOMS"
amount= 10

xoms_dict = {
    "account": account,
    "credits": [
        {
            "account": account,
            "currency": "ARS",
            "amount": amount,
            "settlType": 0
        }
    ],
    "keepPrevious": False
}
def main():
    files = load_files()
    select_file(files, "Monitor de Cuentas")


if __name__ == "__main__":
    main()