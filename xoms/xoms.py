#!/usr/bin/env python
# coding: utf-8

# In[29]:


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
import json

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
    df1 = pd.read_excel(file) #XOMS
    df2 = pd.read_excel(file2) #BOTS
    df1["abs_max"] = df1[["Disponible p/Garantías Opciones Byma", "Disponible p/Garantías MtR"]].max(axis=1)
    df1["min"] = df1[["Disponible p/CI","Disponible p/Garantías MtR"]].min(axis=1)
    df1["Cuenta"]=pd.to_numeric(df1["Cuenta"], errors='coerce').dropna()
    #Drop empty columns
    df2 = df2.dropna(how='all', axis='columns')
    mergedStuff = pd.merge(df1, df2, on=['Cuenta'], how='inner')
    mergedStuff=mergedStuff[["Cuenta","min","Saldo"]]
    mergedStuff["resta"] = mergedStuff["Saldo"]-mergedStuff["min"]
    return mergedStuff

def create_file(mergedStuff):
    xoms= {
        "account": "",
        "credits":[],
        "keepPrevious": True,
    }
    for index, row in mergedStuff.iterrows():
        account_value = int(row['Cuenta'])
        amount_value= row['resta']
        xoms_account = {
            "account": account_value,
            "currency": "ARS",
            "amount": amount_value,
            "settlType": 0
        }
        xoms["credits"].append(xoms_account)
        # print(xoms)
        
    with open("xoms_bots.json", "w") as outfile:
        json.dump(xoms, outfile, indent=4)

def main():
    files = load_files()
    select_file(files, "Monitor de Cuentas")


if __name__ == "__main__":
    main()


# In[30]:


files = load_files()
file = select_file(files, "Monitor de Cuentas")
file2 =select_file(files, "Saldos")
mergedStuff = process(file,file2)
create_file(mergedStuff)

