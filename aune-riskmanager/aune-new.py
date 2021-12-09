##IMPORTS
from argparse import ArgumentParser
import csv
import os, glob, sys
import pandas as pd

def load_files():
    EXTENSIONS_ALLOWED = ['*.xls','*.xlsx','*.csv']
    files_grabbed = []
    for files in EXTENSIONS_ALLOWED:
        files_grabbed.extend(glob.glob(files))
    return files_grabbed

def select_file(files, keyword):
    for file in files:
        if keyword in file:
            return file
def process_aune(file, output_file, keyword):
    if not file:
        return print(f"File not found")
    with open(f"{file}", 'r', newline='') as f, \
    open(f"{output_file}.csv", 'w', newline='') as output_file:
        reader = csv.reader(f, delimiter=';')
        writer = csv.writer(output_file, delimiter= ';')
        flag = False
        print(file,reader)
        for row in reader:
            if keyword in row:
                flag = True
            if flag:
                writer.writerow(row)
                if not row:
                    break

def gvRegistryAccount(file):
    #Leer gvRegistryAccount.xls. Archivo de AP5
    #Skipeamos 1 linea porque aune siempre tiene la 1linea vacia
    if (not os.path.isfile(file) or os.stat(file).st_size == 0):
        return print(f"{file} is empty or does not exist")
    df = pd.read_excel(file)
    df2 = df[['Cuenta', 'Comitente CVSA']]
    return df2

files = load_files()
process_aune(select_file(files, 'Cartera'),"diferencias","Listado de Productos con Interes Abierto, discriminado por comitente")   
process_aune(select_file(files, 'Cartera'),"primas","Listado de Portfolio detallado, discriminando segun origen: Portfolio Anterior (PA), operado en la Rueda (R) y operaciones Simuladas (S)")    
        
gvRegistryAccount = gvRegistryAccount("gvRegistryAccount.xls")